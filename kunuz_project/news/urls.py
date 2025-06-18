from django.urls import path
from .views import NewsListView, KunUzNewsView

urlpatterns = [
    path('news/',       NewsListView.as_view(),   name='news-list'),
    path('kunuz-news/', KunUzNewsView.as_view(),  name='kunuz-news'),
]
