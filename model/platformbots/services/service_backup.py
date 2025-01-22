import redis
import json
import pandas as pd
import os
from django.conf import settings
import logging


# Redis 클라이언트 초기화 (settings.py에 정의된 REDIS_SETTINGS 사용)
logger = logging.getLogger(__name__) # 디버그를 위한 코드
redis_client = redis.Redis(**settings.REDIS_SETTINGS) # 디버그를 위한 코드



class KakaoMessageService:
    @staticmethod
    def format_news_message(article_data):
        # vocab가 문자열인 경우 딕셔너리로 변환
        if isinstance(article_data['vocab'], str):
            try:
                article_data['vocab'] = json.loads(article_data['vocab'])
            except:
                article_data['vocab'] = {}  # 변환 실패시 빈 딕셔너리

        """
        뉴스 데이터를 카카오톡 메시지 형식으로 변환하는 메서드
        
        Args:
            article_data (dict): Redis에서 가져온 뉴스 데이터
                - category: 뉴스 카테고리
                - title: 영문 제목
                - abstract: 한글 제목
                - summary_english: 영문 요약
                - summary_korean: 한글 요약
                - vocab: 단어장 데이터
                - url: 뉴스 링크
        
        Returns:
            str: 포맷팅된 메시지 문자열
        """
        
        message = f"""{article_data['category']} News

title: {article_data['title']}

**English Summary**
- {article_data['summary_english']}

**Korean Summary**
- {article_data['summary_korean']}

**Key Vocabulary**
{KakaoMessageService.format_vocab(article_data['vocab'])}

**Source**
- {article_data['url']}"""
        return message

    @staticmethod
    def format_vocab(vocab):
        try:
            # vocab이 문자열인 경우 변환
            if isinstance(vocab, str):
                vocab = json.loads(vocab)
            return "\n".join([f"* {word} : {meaning}" for word, meaning in vocab.items()])
        except Exception as e:
            print(f"Error formatting vocab: {str(e)}")
            return "* No vocabulary available"

    @staticmethod
    def get_latest_news(category):
        """
        Redis에서 특정 카테고리의 최신 뉴스를 조회하는 메서드
        
        Args:
            category (str): 뉴스 카테고리 (예: 'technology', 'business')
        
        Returns:
            dict: 최신 뉴스 데이터 (없으면 None)
        
        Raises:
            RedisError: Redis 연결 또는 조회 중 오류 발생시
        """
            # 카테고리 매핑
        CATEGORY_MAP = {
            1: 'main',
            2: 'technology',
            3: 'business',
            4: 'science',
            5: 'health',
            6: 'politics',
            7: 'art',
            8: 'sport'
        }
    
        try:
            # category가 정수인 경우 문자열로 변환
            if isinstance(category, int):
                category = CATEGORY_MAP.get(category)
            # 카테고리 유효성 검사
            if not category or not isinstance(category, str):
                logger.error(f"Invalid category: {category}")
                return None
                
            # Redis 키 패턴 생성 및 검색
            redis_key = f"news:{category.lower().strip()}:*"
            redis_articles = redis_client.keys(redis_key)
            
            if not redis_articles:
                logger.info(f"No articles found for category: {category}")
                return None
                
            # 타임스탬프로 정렬하여 최신 기사 선택
            latest_key = sorted(redis_articles, 
                            key=lambda k: redis_client.hget(k, 'timestamp') or 0,
                            reverse=True)[0]
                            
            # 기사 데이터 가져오기
            article_data = redis_client.get(latest_key)
            if not article_data:
                logger.warning(f"Article data not found for key: {latest_key}")
                return None
                
            # JSON 파싱 및 반환
            try:
                article = json.loads(article_data)
                return article
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {str(e)}, data: {article_data}")
                return None
                
        except redis.RedisError as e:
            logger.error(f"Redis error: {str(e)}")
            # Redis 연결 재시도 로직 추가 가능
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None
