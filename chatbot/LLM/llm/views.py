from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import Serializer

@api_view(["GET"])
def json_drf(request):
    # summary: String
    # vocab: dictionary(영단어(string):뜻(string))


    #summary = Article.objects.all()
    #serializer = Serializer(summary, many=True)
    #return Response(serializer.data)

    pass