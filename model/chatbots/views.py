from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from materials.models import News
import redis
import json
from django.conf import settings

redis_client = redis.StrictRedis(**settings.REDIS_SETTINGS)

class SendArticlesToChatbotView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            if not user.is_authenticated:
                return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

            categories = user.categories.all()
            if not categories.exists():
                return Response({'error': 'No categories set for this user'}, status=status.HTTP_400_BAD_REQUEST)

            category_news = {}

            for category in categories:
                viewed_articles_key = f"user:{user.id}:viewed_articles:{category.name}"
                redis_key_pattern = f"news:{category.name.lower()}:*"

                redis_articles = redis_client.keys(redis_key_pattern)
                if redis_articles:
                    redis_articles_data = [
                        json.loads(redis_client.get(article_key))
                        for article_key in redis_articles
                    ]

                    viewed_articles = redis_client.smembers(viewed_articles_key)
                    redis_articles_data = [
                        article for article in redis_articles_data
                        if article['url'] not in viewed_articles
                    ]

                    redis_articles_data.sort(key=lambda article: article.get('created_at', ''), reverse=True)

                    if redis_articles_data:
                        article = redis_articles_data[0]
                        redis_client.sadd(viewed_articles_key, article['url'])
                        redis_client.expire(viewed_articles_key, 7 * 24 * 60 * 60)

                        category_news[category.name] = {
                            "title": article['title'],
                            "abstract": article['abstract'],
                            "summary": {
                                "english": article['summary_english'],
                                "korean": article['summary_korean'],
                            },
                            "vocab": article['vocab'],
                            "url": article['url'],
                            "category": article['category'],
                        }

            if not category_news:
                return Response({"error": "No new articles available for any category."}, status=status.HTTP_404_NOT_FOUND)

            return Response({"articles": category_news}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# chatbots/views.py
'''
class KakaoChatbotView(APIView):
   def post(self, request):
       # 카카오톡 챗봇으로부터 받은 요청 데이터 파싱
       req = request.data
       # intent_name = 설정된 블록의 이름 (사용하지 않는 경우 제거 가능)
       intent_name = req.get('intent', {}).get('name', '')
       # 사용자가 입력한 실제 메시지
       utterance = req.get('userRequest', {}).get('utterance')
       # 사용자의 고유 ID
       user_id = req.get('userRequest', {}).get('user', {}).get('id')

       # 카카오톡 응답을 위한 기본 템플릿 구조
       response = {
           "version": "2.0",
           "template": {
               "outputs": []  # 여러 개의 응답을 배열로 전송 가능
           }
       }

       # 사용자가 "안녕"이라고 입력한 경우의 처리
       if utterance == "안녕":
           response['template']['outputs'].append({
               "simpleText": {
                   "text": "안녕하세요! 원하시는 카테고리를 입력해주세요!"
               }
           })
           return Response(response)

       # 뉴스 정보를 가져와서 응답하는 부분
       try:
           # Redis에서 입력된 카테고리에 해당하는 뉴스 키 검색
           redis_key = f"news:{utterance.lower()}:*"
           redis_articles = redis_client.keys(redis_key)
           
           if redis_articles:
               # 찾은 기사 중 첫 번째(최신) 기사의 데이터를 가져옴
               article_data = json.loads(redis_client.get(redis_articles[0]))
               
               # 카카오톡 응답 메시지 포맷팅
               message = f"""{article_data['category']} News
title: {article_data['title']}
제목: {article_data['abstract']}

**English Summary**
- {article_data['summary_english']}

**Korean Summary**
- {article_data['summary_korean']}

**Key Vocabulary**
{self.format_vocab(article_data['vocab'])}

**Source**
- {article_data['url']}"""

               # 포맷팅된 메시지를 카카오톡 응답 형식에 추가
               response['template']['outputs'].append({
                   "simpleText": {
                       "text": message
                   }
               })
           else:
               # 해당 카테고리의 뉴스가 없는 경우
               response['template']['outputs'].append({
                   "simpleText": {
                       "text": "해당 카테고리의 뉴스를 찾을 수 없습니다."
                   }
               })

       except Exception as e:
           # 에러 발생 시 사용자에게 알림
           response['template']['outputs'].append({
               "simpleText": {
                   "text": "뉴스를 가져오는 중 오류가 발생했습니다."
               }
           })

       return Response(response)

   # 단어장 데이터를 포맷팅하는 헬퍼 함수
   def format_vocab(self, vocab):
       return "\n".join([f"* {word} : {meaning}" for word, meaning in vocab.items()])
'''


# chatbots/views.py
import logging
logger = logging.getLogger(__name__)

class KakaoChatbotView(APIView):
    def post(self, request):
        # 1. 요청 데이터 전체 로깅
        print("=== 전체 요청 데이터 ===")
        print(request.data)
        
        # 2. 구체적인 요청 내용 로깅
        user_message = request.data.get('userRequest', {}).get('utterance', '')
        print(f"사용자 메시지: {user_message}")

        try:
            # 3. 처리 과정 로깅
            print("데이터 처리 시작...")
            # ... 처리 로직 ...
            print("데이터 처리 완료")

            # 4. 응답 데이터 로깅
            response_data = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": f"응답: {user_message}"
                            }
                        }
                    ]
                }
            }
            print("=== 응답 데이터 ===")
            print(response_data)
            
            return Response(response_data)

        except Exception as e:
            # 5. 에러 로깅
            print(f"에러 발생: {str(e)}")
            logger.error(f"상세 에러: {str(e)}", exc_info=True)
            
            return Response({
                "version": "2.0",
                "template": {
                    "outputs": [{"simpleText": {"text": "오류가 발생했습니다."}}]
                }
            })