import redis
import psycopg2
import requests
import time
import json
import csv
from datetime import datetime
from celery import shared_task
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
from chatbots.chatbot import learnChat

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
def fetch_and_store_nyt_news(news_source="NYTimes"):
    API_KEY = settings.NYT_API_KEY
    MAX_RETRIES = 3  
    REQUEST_DELAY = 5  
    TOO_MANY_REQUEST_DELAY = 60  

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
                    title = article.get('title', 'No Title')
                    abstract = article.get('abstract', 'No Abstract')

                    # 요약 및 단어 추출
                    chat = learnChat(abstract)
                    summary_korean = chat.translate(abstract)
                    vocab = chat.vocab()

                    # Redis 저장
                    redis_key = f"news:{category.name.lower()}:{int(time.time())}:{news_url}"
                    redis_value = json.dumps({
                        'title': title,
                        'abstract': abstract,
                        'summary_english': abstract,
                        'summary_korean': summary_korean,
                        'vocab': vocab,
                        'url': news_url,
                        'category': category.name
                    })
                    redis_client.set(redis_key, redis_value, ex=86400)

                    # PostgreSQL 저장
                    News.objects.update_or_create(
                        url=news_url,
                        defaults={
                            'title': title,
                            'abstract': abstract,
                            'summary_english': abstract,
                            'summary_korean': summary_korean,
                            'vocab': vocab,
                            'category': category
                        }
                    )
                break 
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
    # 도커 실행 시 options부터 dirver까지 주석처리
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    #로컬 실행 시 이하 반드시 주석처리(도커에서 크롤링 시 필요한 설정)
    # options = webdriver.ChromeOptions()
    # options.add_argument("--disable-gpu")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")
    # options.add_argument("--window-size=1920,1080")
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    
    # Windows 환경용 설정
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    '''
    driver = webdriver.Chrome(
        service=Service("/usr/local/bin/chromedriver"), 
        options=options
    )
    '''

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
                    title = article.get_text().strip()  # 기사 제목
                    link_element = article.find_parent("a")  # 상위 <a> 태그 찾기
                    link = link_element['href'] if link_element and "href" in link_element.attrs else None

                    # 상대 URL 처리
                    if link and not link.startswith("http"):
                        link = f"https://edition.cnn.com{link}"

                        # 기사 본문 추출
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
        articles = scrape_cnn_news_with_selenium(category_url)

        if articles:
            for article in articles[:5]:  
                if not article['content'] or article['content'].strip() == "" or article['content'] == "No content available.":
                    print(f"article with invalid content: {article['url']}")
                    continue

                chat = learnChat(article['content'])
                summary_english = chat.summarize()
                summary_korean = chat.translate(summary_english)
                vocab = chat.vocab()

                # Redis 저장
                redis_key = f"news:{category.name.lower()}:{int(time.time())}:{article['url']}"
                redis_value = json.dumps({
                    'title': article['title'],
                    'abstract': article['content'],
                    'summary_english': summary_english,
                    'summary_korean': summary_korean,
                    'vocab': vocab,
                    'url': article['url'],
                    'category': category.name
                })
                redis_client.set(redis_key, redis_value, ex=86400)

                # PostgreSQL 저장
                News.objects.update_or_create(
                    url=article['url'],
                    defaults={
                        'title': article['title'],
                        'abstract': article['content'],
                        'summary_english': summary_english,
                        'summary_korean': summary_korean,
                        'vocab': vocab,
                        'category': category,
                    }
                )
            print(f"Saved {len(articles)} articles for category: {category.name}")
        else:
            print(f"No articles found for category: {category.name}")


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
            'task': 'materials.tasks.fetch_and_store_nyt_news',
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