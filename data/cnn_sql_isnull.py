from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd
import sqlite3

# SQLite 데이터베이스 연결 (cnn_news.db 파일 생성됨)
conn = sqlite3.connect('cnn_news.db')
cursor = conn.cursor()

# 뉴스 테이블 생성 (중복 삽입 방지를 위해 UNIQUE 제약 조건 추가)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        link TEXT UNIQUE NOT NULL,
        content TEXT
    )
''')
conn.commit()

def scrape_cnn_news_with_selenium(category, category_url):
    """CNN 뉴스 크롤링"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(category_url)
        
        # 기사 요소 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "container__headline-text"))
        )
        
        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = []

        # 기사 제목과 링크 추출
        for article in soup.find_all('span', class_='container__headline-text')[:5]:
            title = article.get_text().strip()  # 기사 제목
            link_element = article.find_parent("a")  # 상위 <a> 태그 찾기
            link = link_element['href'] if link_element and "href" in link_element.attrs else None

            # 상대 URL 처리
            if link and not link.startswith("http"):
                link = f"https://edition.cnn.com{link}"

                # 기사 본문 추출
                content = extract_article_content(driver, link)

                # 기사 데이터 저장
                articles.append({"category": category, "title": title, "link": link, "content": content})

        return articles

    except Exception as e:
        print(f"Error occurred while scraping {category_url}: {e}")
        return []
    
    finally:
        driver.quit()  # 브라우저 종료

def extract_article_content(driver, article_url):
    """기사의 전문 추출"""
    try:
        driver.get(article_url)
        time.sleep(3)  # 페이지 로딩 대기
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 본문 내용 추출
        paragraphs = soup.find_all('p', class_='paragraph inline-placeholder vossi-paragraph')
        content = " ".join([p.get_text().strip() for p in paragraphs])
        return content[:500] + "..." if len(content) > 500 else content
    except Exception as e:
        print(f"Error while extracting content from {article_url}: {e}")
        return "No content available."

def save_to_db(news_list):
    """SQLite에 뉴스 데이터 저장"""
    for article in news_list:
        try:
            cursor.execute('''
                INSERT INTO news (category, title, link, content)
                VALUES (?, ?, ?, ?)
            ''', (article['category'], article['title'], article['link'], article['content']))
        except sqlite3.IntegrityError:
            print(f"Skipping duplicate: {article['title']}")
    
    conn.commit()  # 변경 사항 저장

# 카테고리 목록
categories = {
    "world": "https://edition.cnn.com/world",
    "business": "https://edition.cnn.com/business",
    "science": "https://edition.cnn.com/science",
    "health": "https://edition.cnn.com/health",
    "politics": "https://edition.cnn.com/politics",
    "entertainment": "https://edition.cnn.com/entertainment",
    "sport": "https://edition.cnn.com/sport"
}

# 전체 뉴스 데이터를 저장할 리스트 초기화
cnn_news = []

# 크롤링 및 저장 실행
for category, url in categories.items():
    print(f"Fetching articles for category: {category}")
    articles = scrape_cnn_news_with_selenium(category, url)
    
    if articles:
        cnn_news.extend(articles)
        save_to_db(articles)
        for article in articles[:1]:  # 상위 1개 기사만 출력
            print(f"Title: {article['title']}\nLink: {article['link']}\nContent: {article['content'][:200]}...\n")
    else:
        print(f"No articles found for category: {category}")
    print("="*50)

# 데이터프레임으로 변환 및 CSV 저장
if cnn_news:
    df = pd.DataFrame(cnn_news)
    
    # CSV 파일로 저장
    csv_file_name = 'cnn_news.csv'
    df.to_csv(csv_file_name, index=False, encoding='utf-8-sig')
    print(f"\nSaved {len(cnn_news)} articles to {csv_file_name}")
else:
    print("No news data to save.")

# DB 연결 종료
conn.close()
print("\nAll data saved to SQLite database (cnn_news.db).")
