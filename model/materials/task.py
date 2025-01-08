from celery import shared_task
from datetime import datetime
import redis
import psycopg2
from decouple import config

# Redis 설정
redis_client = redis.StrictRedis(
    host='127.0.0.1',
    port=6379,
    db=1,
    decode_responses=True
)

# PostgreSQL 연결 설정
def get_postgres_connection():
    return psycopg2.connect(
        dbname=config("POSTGRES_DB"),
        user=config("YOUR_POSTGRESQL_USERNAME"),
        password=config("YOUR_POSTGRESQL_PASSWORD"),
        host="127.0.0.1",
        port="5432"
    )

@shared_task
def transfer_data_to_postgresql():
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()

        # Redis 데이터 가져오기
        keys = redis_client.keys('news:*')  
        for key in keys:
            news_id = key.split(':')[1] 
            content = redis_client.get(key)
            
            # PostgreSQL에 데이터 저장
            cursor.execute(
                """
                INSERT INTO news (id, content, created_at)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
                """,
                (news_id, content, datetime.now())
            )
            redis_client.delete(key)  # Redis에서 데이터 삭제

        conn.commit()
        print(f"[{datetime.now()}] Data transfer complete. {len(keys)} items moved.")
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

#celery 작동 확인용 함수
@shared_task
def example_task():
    print("Test task executed!")
    return "Task completed"

# def crawl_news():
#     # 크롤링 로직 나오면 ㅊ ㅜ가하기 
#     print(f"[{datetime.now()}] News crawling completed.")
