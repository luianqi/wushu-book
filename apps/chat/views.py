from rest_framework.viewsets import ModelViewSet

from apps.chat.models import Room, Message
from apps.chat.serializers import RoomSerializer, MessageSerializer


class RoomView(ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()


class MessageView(ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

