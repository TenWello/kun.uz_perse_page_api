from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import News
from .serializers import NewsSerializer

class NewsListView(generics.ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        queryset = News.objects.all().order_by('-id')
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)
        return queryset

class KunUzNewsView(APIView):
    def get(self, request):
        main_news   = News.objects.filter(type='main').order_by('-id')[:1]
        return Response({
            "main":   NewsSerializer(main_news,   many=True).data
            # "latest": NewsSerializer(latest_news, many=True).data # Agar left + right side kk bolsa
        })
