from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.db.models import Count
from .models import Posts, Comment, Like, KarmaTransaction
from .serializers import PostSerializer, CommentSerializer
from rest_framework import status
from django.db import IntegrityError, transaction

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
        .annotate(like_count=Count("likes"))
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

@api_view(['POST'])
def like_post(request, post_id):
    user = request.user

    try:
        post = Posts.objects.get(id=post_id)
    except Posts.DoesNotExist:
        return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        with transaction.atomic():
            Like.objects.create(user=user, post=post)

            KarmaTransaction.objects.create(
                user=post.author,
                points=5
            )

            return Response(
                {"message": "Post liked successfully."},
                status=status.HTTP_201_CREATED
            )
        
    except IntegrityError:
        return Response(
            {"error": "You have already liked this post."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
@api_view(['POST'])
def like_comment(request, comment_id):
    user = request.user

    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        with transaction.atomic():
            Like.objects.create(user=user, comment=comment)

            KarmaTransaction.objects.create(
                user = comment.author,
                points=1
            )

            return Response(
                {"message": "Comment liked"},
                status=status.HTTP_201_CREATED
            )
        
    except IntegrityError:
        return Response(
            {"error": "You have already liked this comment."},
            status=status.HTTP_400_BAD_REQUEST
        )