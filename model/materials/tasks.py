import redis
import psycopg2
import requests
import time
import json
import csv
from datetime import datetime
from celery import shared_task
from decouple import config
from accounts.models import Category
from materials.models import News
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from django.db import transaction
from psycopg2 import sql

from django.conf import settings

redis_client = redis.StrictRedis(**settings.REDIS_SETTINGS)


# postgresql 설정
def get_postgres_connection():
    db_config = settings.DATABASES['default']
    return psycopg2.connect(
        dbname=db_config['NAME'],
        user=db_config['USER'],
        password=db_config['PASSWORD'],
        host=db_config['HOST'],
        port=db_config['PORT']
    )

# nyt api에서 받아와 db에 저장
@shared_task
def fetch_and_store_news(news_source="NYTimes"):
    API_KEY = config("NYT_API_KEY")
    MAX_RETRIES = 3  # 최대 재시도 횟수
    REQUEST_DELAY = 5  # 기본 요청 간 대기 시간 (초)
    TOO_MANY_REQUEST_DELAY = 60  # Too Many Requests 시 대기 시간 (초)

    categories = Category.objects.all()
    if not categories.exists():
        print("No categories found in the database.")
        return

    for category in categories:
        source_category = category.get_source_category(category.name, news_source)
        if not source_category:
            print(f"No mapping found for category '{category.name}' in source '{news_source}'.")
            continue

        url = f"https://api.nytimes.com/svc/topstories/v2/{source_category}.json"
        params = {'api-key': API_KEY}
        
        retries = 0
        while retries < MAX_RETRIES:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                articles = data.get('results', [])
                print(f"Fetching articles for category: {category.name} ({source_category})")

                for article in articles[:5]:
                    news_url = article.get('url', 'No URL')
                    redis_key = f"news:{category.name.lower()}:{news_url}"
                    redis_value = json.dumps({
                        'title': article.get('title', 'No Title'),
                        'abstract': article.get('abstract', 'No Abstract'),
                        'url': news_url,
                        'published_date': article.get('published_date', 'No Date'),
                        'category': category.name
                    })

                    
                    redis_client.set(redis_key, redis_value, ex=86400)

                
                    News.objects.update_or_create(
                        url=news_url,
                        defaults={
                            'title': article.get('title', 'No Title'),
                            'abstract': article.get('abstract', 'No Abstract'),
                            'published_date': article.get('published_date', 'No Date'),
                            'category': category
                        }
                    )

                break  # 성공하면 반복 종료
            elif response.status_code == 429:
                print(f"Too many requests for category: {category.name}. Retrying in {TOO_MANY_REQUEST_DELAY} seconds...")
                time.sleep(TOO_MANY_REQUEST_DELAY)
            else:
                print(f"Failed to fetch articles for category: {category.name}. Status Code: {response.status_code}")
                retries += 1
                time.sleep(REQUEST_DELAY)

        if retries == MAX_RETRIES:
            print(f"Max retries reached for category: {category.name}. Skipping...")
        time.sleep(REQUEST_DELAY)


#cnn크롤링
def scrape_cnn_news_with_selenium(category_url, max_retries=1, retry_delay=5):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        retries = 0
        while retries < max_retries:
            try:
                driver.get(category_url)

                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "container__headline-text"))
                )

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                articles = []

                for article in soup.find_all('span', class_='container__headline-text')[:5]:
                    title = article.get_text().strip()
                    link_element = article.find_parent("a")
                    if link_element and "href" in link_element.attrs:
                        link = link_element['href']
                        if not link.startswith("http"):
                            link = f"https://edition.cnn.com{link}"

                        # 기사 전문 추출
                        content = extract_article_content(driver, link)

                        articles.append({"title": title, "url": link, "content": content})

                return articles

            except Exception as e:
                retries += 1
                print(f"Attempt {retries}/{max_retries} failed for {category_url}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)

        print(f"Max retries reached for {category_url}. Skipping...")
        return []

    except Exception as e:
        print(f"Error occurred while scraping {category_url}: {e}")
        return []

    finally:
        driver.quit()


#cnn 기사 전문추출
def extract_article_content(driver, article_url, max_retries=1, retry_delay=5):
    retries = 0
    while retries < max_retries:
        try:
            driver.get(article_url)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            paragraphs = soup.find_all('p', class_='paragraph inline-placeholder vossi-paragraph')
            content = " ".join([p.get_text().strip() for p in paragraphs])
            return content  

        except Exception as e:
            retries += 1
            print(f"Attempt {retries}/{max_retries} failed for {article_url}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

    print(f"Max retries reached for {article_url}. Returning 'No content available.'")
    return "No content available."


@shared_task
def fetch_and_store_cnn_news():
    categories = Category.objects.all()
    if not categories.exists():
        print("No categories found in the database.")
        return

    for category in categories:
        source_category = category.get_source_category(category.name, "CNN")
        if not source_category:
            print(f"No mapping found for category '{category.name}' in source 'CNN'.")
            continue

        category_url = f"https://edition.cnn.com/{source_category}"
        print(f"Fetching articles for category: {category.name} (URL: {category_url})")

        articles = scrape_cnn_news_with_selenium(category_url)

        if articles:
            for article in articles[:5]:  
                redis_key = f"news:{category.name.lower()}:{article['url']}"
                redis_value = json.dumps({
                    'title': article['title'],
                    'abstract': article['content'],  # CNN 기사 전문을 abstract로 저장
                    'url': article['url'],
                    'published_date': time.strftime('%Y-%m-%d %H:%M:%S'),  
                    'category': category.name
                })
                redis_client.set(redis_key, redis_value, ex=86400)  

                # PostgreSQL 저장
                News.objects.update_or_create(
                    url=article['url'],
                    defaults={
                        'title': article['title'],
                        'abstract': article['content'],  # CNN 기사 전문
                        'published_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'category': category,
                    }
                )
            print(f"Saved {len(articles)} articles for category: {category.name}")
        else:
            print(f"No articles found for category: {category.name}")


# csv파일로 저장
def save_redis_to_csv(file_name="news_data.csv"):
    keys = redis_client.keys('news:*')
    if not keys:
        print("No data in Redis to save.")
        return

    with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Title', 'Abstract', 'URL', 'Published Date', 'Category']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for key in keys:
            news_data = json.loads(redis_client.get(key))
            writer.writerow({
                'Title': news_data.get('title', ''),
                'Abstract': news_data.get('abstract', ''),
                'URL': news_data.get('url', ''),
                'Published Date': news_data.get('published_date', ''),
                'Category': news_data.get('category', '')
            })

    print(f"Data successfully saved to {file_name}.")

# celery task: redis 데이터 csv로 저장
@shared_task
def save_news_to_csv_task(file_name="news_data.csv"):
    save_redis_to_csv(file_name=file_name)


def setup_periodic_tasks():
    try:
        schedule = IntervalSchedule.objects.get(every=1, period=IntervalSchedule.DAYS)
    except IntervalSchedule.MultipleObjectsReturned:
        schedules = IntervalSchedule.objects.filter(every=1, period=IntervalSchedule.DAYS)
        schedule = schedules.first()
        schedules.exclude(id=schedule.id).delete()
    except IntervalSchedule.DoesNotExist:
        schedule = IntervalSchedule.objects.create(every=1, period=IntervalSchedule.DAYS)

    # NYTimes 작업
    PeriodicTask.objects.update_or_create(
        name='Fetch and Store NYT News Daily',
        defaults={
            'interval': schedule,
            'task': 'materials.tasks.fetch_and_store_news',
            'args': '[]',
            'kwargs': '{}',
            'enabled': True,
        },
    )

    # CNN 작업
    PeriodicTask.objects.update_or_create(
        name='Fetch and Store CNN News Daily',
        defaults={
            'interval': schedule,
            'task': 'materials.tasks.fetch_and_store_cnn_news',
            'args': '[]',
            'kwargs': '{}',
            'enabled': True,
        },
    )