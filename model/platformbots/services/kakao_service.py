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
        
        message = (
                  f"{article_data['category']} News\n"

                  f"title: {article_data['title']}\n\n"
                  
                  f"**English Summary**\n"
                  f"- {article_data['summary_english']}\n\n"
                  
                  f"**Korean Summary**\n"
                  f"- {article_data['summary_korean']}\n\n"
                  
                  f"**Key Vocabulary**\n"
                  f"{KakaoMessageService.format_vocab(article_data['vocab'])}\n\n"
                  
                  f"**Source**\n"
                  f"- {article_data['url']}"
                )
                
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
            
            if not category or not isinstance(category, str):
                logger.error(f"Invalid category: {category}")
                return None
            
            # 키 패턴 수정
            redis_key_pattern = f"news:{category.lower().strip()}:*:*"  # 타임스탬프와 URL 패턴 포함
            
            # keys() 대신 scan_iter() 사용
            keys = list(redis_client.scan_iter(match=redis_key_pattern))
            logger.info(f"Category: {category}, Found keys: {keys}")  # 추가


            if not keys:
                logger.error(f"No keys found for pattern: {redis_key_pattern}")  # 추가
                return None
                
            # 타임스탬프로 정렬
            sorted_keys = sorted(keys, key=lambda k: k.split(':')[2], reverse=True)
            
            # 최신 4개 키만 선택
            recent_keys = sorted_keys[:4]

            # 4개 중 랜덤 선택
            import random

            latest_key = random.choice(recent_keys)


            # 데이터 가져오기 (문자열로 저장된 데이터)
            article_data_str = redis_client.get(latest_key)
            
            if not article_data_str:
                logger.warning(f"Article data not found for key: {latest_key}")
                return None
            
            # JSON 문자열을 딕셔너리로 변환
            article = json.loads(article_data_str)
            
            return article
        
        except redis.RedisError as e:
            logger.error(f"Redis error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None
        
    # 헤드라인 기능추가
    @staticmethod
    def get_headlines():
        try:
            # main 카테고리 뉴스 키 조회
            redis_key_pattern = "news:main:*:*"
            keys = list(redis_client.scan_iter(match=redis_key_pattern))
            
            # 타임스탬프로 정렬하여 최신 5개 선택
            sorted_keys = sorted(keys, key=lambda k: k.split(':')[2], reverse=True)[:5]
            
            headlines = []
            for key in sorted_keys:
                article_data = json.loads(redis_client.get(key))
                headlines.append({
                    'title': article_data['title'],
                    'url': article_data['url']
                })
            
            # 메시지 포맷팅
            message = "오늘의 헤드라인 뉴스를 전해드려요!\n\n"
            for headline in headlines:
                message += f"{headline['title']}\n{headline['url']}\n\n"
                
            return message
        except Exception as e:
            logger.error(f"Error getting headlines: {str(e)}")
            return None