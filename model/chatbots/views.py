from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from materials.models import News
import redis
import json

# Redis 클라이언트 설정
redis_client = redis.StrictRedis(
    host='127.0.0.1',
    port=6379,
    db=1,
    decode_responses=True
)

class SendArticlesToChatbotView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = request.user  
            if not user.is_authenticated:
                return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

            categories = user.categories.all()
            if not categories.exists():
                return Response({'error': 'No categories set for this user'}, status=status.HTTP_400_BAD_REQUEST)

            # 우선 관심사가 여러개면 첫번째 관심사를 가져오게 설정했습니다 
            category = categories.first()

            # Redis에서 사용자가 본 기사 ID 가져오기
            viewed_articles_key = f"user:{user.id}:viewed_articles:{category.name}"
            viewed_articles = redis_client.smembers(viewed_articles_key)  

            # 사용자가 본 기사 제외, 관심사에 맞는 새로운 기사 조회
            article = News.objects.filter(
                category=category
            ).exclude(id__in=viewed_articles).order_by('published_date').first()

            if not article:
                return Response({"error": "No new articles available for this category."}, status=status.HTTP_404_NOT_FOUND)

            # Redis에 사용자가 본 기사 ID 추가
            redis_client.sadd(viewed_articles_key, article.id)
            redis_client.expire(viewed_articles_key, 7 * 24 * 60 * 60)

            article_data = {
                "article_id": article.id,
                "title": article.title,
                "content": article.abstract,
                "category": article.category.name,
                "url": article.url,
                "published_date": article.published_date.strftime('%Y-%m-%d %H:%M:%S')
            }

            return Response({"article": article_data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
