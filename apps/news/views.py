from rest_framework import generics
from rest_framework.filters import SearchFilter

from apps.news.serializers import NewsSerializer
from apps.news.models import News


class NewsView(generics.ListCreateAPIView):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description', 'created_date']


class DeleteNewsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsSerializer
    queryset = News.objects.all()

