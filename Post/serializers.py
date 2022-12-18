from rest_framework import serializers
from .models import Post,Comment,PostImage,Category
from Account.serializers import UserSerializer


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model= PostImage
        fields = ["id","image"] 

class CommentSerializer(serializers.ModelSerializer):
    comment_by = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ["id","comment_by","comment"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    user =UserSerializer(read_only=True)
    postimage = PostImageSerializer(many=True,read_only=True)
    like_by = UserSerializer(many=True,read_only=True)
    comment = CommentSerializer(many=True,read_only=True)
    category = CategorySerializer(many=True,read_only=True)
    saved_by = UserSerializer(many=True,read_only=True)
    class Meta:
        model = Post
        fields = '__all__'