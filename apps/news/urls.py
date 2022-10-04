from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.news.views import DeleteNewsView, NewsView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path("createnew/", NewsView.as_view(), name="create_new"),
    path("deletenew/<int:pk>", DeleteNewsView.as_view(), name="delete_news")
]
