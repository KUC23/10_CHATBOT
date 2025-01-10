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

# Redis 설정
redis_client = redis.StrictRedis(
    host='127.0.0.1',
    port=6379,
    db=1,
    decode_responses=True
)

# postgresql 설정
def get_postgres_connection():
    return psycopg2.connect(
        dbname=config("POSTGRES_DB"),
        user=config("YOUR_POSTGRESQL_USERNAME"),
        password=config("YOUR_POSTGRESQL_PASSWORD"),
        host="127.0.0.1",
        port="5432"
    )

# nyt api에서 받아와 redis에 저장
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

# redis의 데이터 postgresql로 이동
@shared_task
def transfer_data_to_postgresql():
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()

        keys = redis_client.keys('news:*')
        for key in keys:
            news_data = json.loads(redis_client.get(key))
            news_id = key.split(':')[2]
            title = news_data.get('title', '')
            abstract = news_data.get('abstract', '')
            url = news_data.get('url', '')
            published_date = news_data.get('published_date', '')
            category_name = news_data.get('category', '')

            category, _ = Category.objects.get_or_create(name=category_name)

            # PostgreSQL에 데이터 저장
            cursor.execute(
                """
                INSERT INTO materials_news (id, title, abstract, url, published_date, category_id, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
                """,
                (news_id, title, abstract, url, published_date, category.id, datetime.now())
            )
            redis_client.delete(key)

        conn.commit()
        print(f"[{datetime.now()}] Data transfer complete. {len(keys)} items moved.")
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

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
    # Interval Schedule 생성
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,
    )

    # PeriodicTask 생성
    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name='Fetch and Store News Daily',
        task='tasks.fetch_and_store_news',
    )