from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.db.models import Count
from .models import Posts
from .serializers import PostSerializer

# Create your views here.
@api_view(['GET'])
def me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
def feed(request):
    posts = (
        Posts.objects
        .select_related('author')
        .order_by('-created_at')
    )

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)