from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import redis

redis_client = redis.StrictRedis(
    host='127.0.0.1',
    port=6379,
    db=1,
    decode_responses=True
)

class NewsView(APIView):
    #redis에서 관심사에 맞는 뉴스 조회기능
    def get(self, request, *args, **kwargs):
        user = request.user  
        if not user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)
        
        categories = user.categories.all()
        if not categories.exists():
            return Response({'error': 'No categories set for this user'}, status=400)
        
        category_news = {}
        for category in categories:
            keys = redis_client.keys(f'news:{category.name}:*')[:5]  #레디스에 저장된 키 형태: ex)news:technology:1
            news_list = [redis_client.get(key) for key in keys]
            category_news[category.name] = news_list #category_news={"technology":[기사1, 기사2..], "health":[기사1, 기사2..]..}

        return Response({'user_categories': category_news})
        
    #redis에 뉴스 저장기능
    def post(self, request, *args, **kwargs):
        category = request.data.get('category', 'Main') 
        news_id = request.data.get('id', '1')
        content = request.data.get('content', '')

        redis_client.set(f'news:{category}:{news_id}', content)
        return Response({'message': 'News saved!', 'category': category, 'id': news_id})




#정보전송로직에서 소셜계정선택
# default_provider = user.default_social_provider
# if not default_provider:
#     # 기본 제공 계정이 설정되지 않았다면 첫 번째 연결된 계정을 사용하도록
#     default_provider = user.connected_social_providers[0]



