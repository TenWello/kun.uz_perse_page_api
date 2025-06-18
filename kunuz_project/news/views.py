from rest_framework import generics
from .models import News
from .serializers import NewsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class NewsListView(generics.ListAPIView):
    queryset = News.objects.all().order_by('-id')
    serializer_class = NewsSerializer

class KunUzNewsView(APIView):
    def get(self, request):
        main_news   = News.objects.filter(type='main').order_by('-id')[:1]
        return Response({
            "main":   NewsSerializer(main_news,   many=True).data
            # "latest": NewsSerializer(latest_news, many=True).data # Agar left + right side kk bolsa
        })
