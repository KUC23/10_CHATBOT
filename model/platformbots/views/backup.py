from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ..services.kakao_service import KakaoMessageService
import logging
logger = logging.getLogger(__name__)

'''
디버깅용 클래스
class KakaoWebhookView(APIView):
    """
    카카오톡 챗봇 웹훅을 처리하는 뷰
    카카오톡 스킬 서버로 등록되어 사용자 메시지를 처리하고 응답을 반환
    """
    def post(self, request):
        logger.debug(f"Received request: {request.data}")
        # 카카오톡 응답 기본 템플릿
        response = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "기본 응답입니다."
                        }
                    }
                ]
            }
        }

        try:
            # 디버깅을 위한 요청 데이터 출력
            print("Received request data:", request.data)
            req = request.data
            utterance = req.get('userRequest', {}).get('utterance', '')

            if utterance == "안녕":
                response['template']['outputs'][0]['simpleText']['text'] = "안녕하세요! 반갑습니다."
                
        except Exception as e:
            print(f"Error: {str(e)}")
            response['template']['outputs'][0]['simpleText']['text'] = "오류가 발생했습니다."
        logger.debug(f"Sending response: {response}")
        return Response(response)
'''



class KakaoWebhookView(APIView):
    def post(self, request):
        # 카카오톡 응답 기본 템플릿
        response = {
            "version": "2.0",
            "template": {
                "outputs": []
            }
        }

        try:
            # 카카오톡으로부터 받은 요청 데이터 파싱
            req = request.data
            # userRequest.utterance: 사용자가 입력한 메시지
            utterance = req.get('userRequest', {}).get('utterance', '')

            # 인사 처리
            if utterance == "안녕":
                response['template']['outputs'].append({
                    "simpleText": {
                        "text": "안녕하세요! 원하시는 카테고리를 입력해주세요"
                    }
                })
                return Response(response)
            
            # 카테고리 입력 시 해당 뉴스 제공
            article = KakaoMessageService.get_latest_news(utterance)
            if article:
                # 뉴스 데이터를 카카오톡 메시지 형식으로 변환
                message = KakaoMessageService.format_news_message(article)
                response['template']['outputs'].append({
                    "simpleText": {
                        "text": message
                    }
                })
            else:
                # 해당 카테고리 뉴스가 없는 경우
                response['template']['outputs'].append({
                    "simpleText": {
                        "text": "해당 카테고리의 뉴스를 찾을 수 없습니다."
                    }
                })

        except Exception as e:
            # 에러 로깅 및 사용자에게 에러 메시지 전송
            print(f"Error processing request: {str(e)}")
            response['template']['outputs'].append({
                "simpleText": {
                    "text": "처리 중 오류가 발생했습니다."
                }
            })

        return Response(response)
    


    import redis
import json
import pandas as pd
import os
from django.conf import settings
import logging
import redis


# Redis 클라이언트 초기화 (settings.py에 정의된 REDIS_SETTINGS 사용)
# redis_client = redis.StrictRedis(**settings.REDIS_SETTINGS)


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

'''
    @staticmethod
    def get_latest_news(category):
        """
        CSV 파일에서 특정 카테고리의 뉴스를 조회하는 메서드
        테스트용으로 제작
        
        Args:
            category (str): 뉴스 카테고리 (예: 'technology', 'business')
        
        Returns:
            dict: 해당 카테고리의 뉴스 데이터 (없으면 None)
        """
        try:
            csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'news_data.csv')
            try:
                df = pd.read_csv(csv_path, encoding='utf-8')  # 혹시나 모를 인코딩 문제 해결
            except:
                df = pd.read_csv(csv_path, encoding='cp949')
            
            # 현재 카테고리 목록 확인
            print(f"사용 가능한 카테고리: {df['category'].unique()}")
            
            # 공백 제거 후 비교
            category_news = df[df['category'].str.strip().str.lower() == category.strip().lower()]
            
            if not category_news.empty:
                news = category_news.iloc[0].to_dict()
                return news
                
            return None
                
        except Exception as e:
            print(f"Error reading CSV: {str(e)}")
            import traceback
            print(traceback.format_exc())  # 상세 에러 정보 출력
            return None
'''

logger = logging.getLogger(__name__) # 디버그를 위한 코드
redis_client = redis.Redis(**settings.REDIS_SETTINGS) # 디버그를 위한 코드

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
    try:
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


'''
    @staticmethod
    ### Redis에서 특정 카테고리의 최신 뉴스를 조회하는 메서드 ###
    def get_latest_news(category):

        """
        Redis에서 특정 카테고리의 최신 뉴스를 조회하는 메서드
        
        Args:
            category (str): 뉴스 카테고리 (예: 'technology', 'business')
        
        Returns:
            dict: 최신 뉴스 데이터 (없으면 None)
        """
        # Redis 키 패턴: "news:카테고리:URL"
        redis_key = f"news:{category.lower()}:*"
        redis_articles = redis_client.keys(redis_key)
        
        if redis_articles:
            # 가장 최근 기사 가져오기
            latest_article = json.loads(redis_client.get(redis_articles[0]))
            return latest_article
        return None
'''