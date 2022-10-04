from rest_framework import serializers

from apps.account.serializers import RegisterUserSerializer
from apps.chat.models import Message, Room


class MessageSerializer(serializers.ModelSerializer):
    user = RegisterUserSerializer

    class Meta:
        model = Message
        fields = [
            "id",
            "room",
            "text",
            "user",
            "created_at"
        ]


class RoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = [
            "id",
            "name",
            "host",
            "messages",
            "current_users",
            "last_message"
        ]
        # depth = 1
        read_only_fields = ["messages", "last_message"]

    def get_last_message(self, obj: Room):
        return MessageSerializer(obj.messages.order_by("created_at").last()).data





