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



