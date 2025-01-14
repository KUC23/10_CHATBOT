from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd

def scrape_cnn_news_with_selenium(category_url):
    # Selenium WebDriver 설정
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
        for article in soup.find_all('span', class_='container__headline-text'):
            title = article.get_text().strip()  # 기사 제목
            link_element = article.find_parent("a")  # 상위 <a> 태그 찾기
            if link_element and "href" in link_element.attrs:
                link = link_element['href']
                if not link.startswith("http"):  # 상대 경로 처리
                    link = f"https://edition.cnn.com{link}"

                # 기사 본문 전문 추출
                content = extract_article_content(driver, link)

                articles.append({"title": title, "link": link, "content": content})

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
        return content
    except Exception as e:
        print(f"Error while extracting content from {article_url}: {e}")
        return "No content available."


# 카테고리
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

# 결과 출력
for category, url in categories.items():
    print(f"Fetching articles for category: {category}")
    articles = scrape_cnn_news_with_selenium(url)
    
    if articles:
        cnn_news.extend(articles)
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
