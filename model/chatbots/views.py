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
                viewed_articles = redis_client.smembers(viewed_articles_key)

                article = News.objects.filter(
                    category=category
                ).exclude(id__in=viewed_articles).order_by('published_date').first()

                if article:
                    # Redis에 사용자가 본 기사 ID 추가
                    redis_client.sadd(viewed_articles_key, article.id)
                    redis_client.expire(viewed_articles_key, 7 * 24 * 60 * 60)

                    category_news[category.name] = {
                        "article_id": article.id,
                        "title": article.title,
                        "content": article.abstract,
                        "category": article.category.name,
                        "url": article.url,
                        "published_date": article.published_date.strftime('%Y-%m-%d %H:%M:%S')
                    }

            if not category_news:
                return Response({"error": "No new articles available for any category."}, status=status.HTTP_404_NOT_FOUND)

            return Response({"articles": category_news}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

