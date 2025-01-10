from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from materials.models import News
from accounts.models import Category
import redis
import json

redis_client = redis.StrictRedis(
    host='127.0.0.1',
    port=6379,
    db=1,
    decode_responses=True
)

class NewsView(APIView):
    # 유저 관심사에 맞는 뉴스 조회(redis 먼저 확인 후 postgresql)
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            if not user.is_authenticated:
                return Response({'error': 'Authentication required'}, status=401)

            categories = user.categories.all()
            if not categories.exists():
                return Response({'error': 'No categories set for this user'}, status=400)

            category_news = {}
            for category in categories:
                keys = list(redis_client.scan_iter(f'news:{category.name.lower()}:*', count=5))
                news_list = []

                for key in keys:
                    news_data = redis_client.get(key)
                    if news_data:
                        news_list.append(json.loads(news_data))

                # Redis에 데이터가 없으면 PostgreSQL에서 조회
                if not news_list:
                    news_objects = News.objects.filter(category=category).order_by('-published_date')[:5]
                    news_list = [
                        {
                            'title': news.title,
                            'abstract': news.abstract,
                            'url': news.url,
                            'published_date': news.published_date.strftime('%Y-%m-%d %H:%M:%S'),
                            'category': news.category.name
                        }
                        for news in news_objects
                    ]

                    # PostgreSQL 데이터를 Redis에 저장
                    for news in news_list:
                        redis_key = f"news:{category.name.lower()}:{news['url']}"
                        redis_client.set(redis_key, json.dumps(news), ex=86400)

                category_news[category.name] = news_list

            return Response({'user_categories': category_news})
        except redis.RedisError as e:
            return Response({'error': f'Redis error: {str(e)}'}, status=500)
        except Exception as e:
            return Response({'error': f'Unexpected error: {str(e)}'}, status=500)