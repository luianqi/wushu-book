from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.chat.views import RoomView, MessageView

router = DefaultRouter()
router.register(r'room', RoomView)
router.register(r'message', MessageView)


urlpatterns = [
    path('', include(router.urls)),
]