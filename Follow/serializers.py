from Follow.models import Friend
from rest_framework import serializers
from Account.serializers import UserSerializer

class AllFriend(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    followers = UserSerializer(many=True,read_only=True)
    following = UserSerializer(many=True,read_only=True)
    mutual = UserSerializer(many=True,read_only=True)
    class Meta:
        model = Friend
        fields = '__all__'
