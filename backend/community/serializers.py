from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Posts, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Posts
        fields = ['id', 'author', 'content', 'created_at', 'like_count']

    def get_like_count(self, obj):
        return obj.like_count

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'children']
    
    def get_children(self, obj):
        return []
