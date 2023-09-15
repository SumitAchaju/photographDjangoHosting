from rest_framework import serializers
from .models import Message
from Account.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    send_user = UserSerializer(read_only=True)
    receive_user = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['id','message_type','message_text','message_img','send_user','receive_user','send_date','msg_status','formated_date']