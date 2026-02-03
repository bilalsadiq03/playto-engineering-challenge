from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.db.models import Count
from .models import Posts, Comment
from .serializers import PostSerializer, CommentSerializer

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

@api_view(['GET'])
def post_comments(request, post_id):
    post = Posts.objects.get(id=post_id)

    comments = (
        Comment.objects
        .filter(post=post)
        .select_related('author')
        .order_by('created_at')
    )

    comment_map = {}
    roots = []

    for comment in comments:
        comment_map[comment.id] = {
            "id": comment.id,
            "author": comment.author.username,
            "content": comment.content,
            "created_at": comment.created_at,
            "children": []
        }

    for comment in comments:
        if comment.parent_id:
            comment_map[comment.parent_id]["children"].append(
                comment_map[comment.id]
            )
        else:
            roots.append(comment_map[comment.id])

    return Response(roots)
