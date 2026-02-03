from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes, IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import  AllowAny
from rest_framework.authentication import BasicAuthentication
from .serializers import UserSerializer
from django.db.models import Count, Sum
from .models import Posts, Comment, Like, KarmaTransaction
from .serializers import PostSerializer, CommentSerializer
from rest_framework import status
from django.db import IntegrityError, transaction
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

# Create your views here.
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"detail": "Username and password required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {"detail": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    login(request, user)

    return Response(
        {"detail": "Login successful"},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(["POST"])
def create_post(request):
    content = request.data.get("content")

    if not content or not content.strip():
        return Response(
            {"error": "Content is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    post = Posts.objects.create(
        author=request.user,
        content=content
    )

    serializer = PostSerializer(post)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def create_comment(request, post_id):
    content = request.data.get("content")
    parent_id = request.data.get("parent")

    if not content or not content.strip():
        return Response(
            {"error": "Content is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        post = Posts.objects.get(id=post_id)
    except Posts.DoesNotExist:
        return Response(
            {"error": "Post not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    parent = None
    if parent_id:
        try:
            parent = Comment.objects.get(id=parent_id)
        except Comment.DoesNotExist:
            return Response(
                {"error": "Parent comment not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

    comment = Comment.objects.create(
        post=post,
        author=request.user,
        content=content,
        parent=parent
    )

    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


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
    
@api_view(['POST'])
def leaderboard(request):
    since = timezone.now() - timezone.timedelta(hours=24)

    qs = (
        KarmaTransaction.objects
        .filter(created_at__gte=since)
        .values("user__username")
        .annotate(karma=Sum("points"))
        .order_by("-karma")[:5]
    )

    leaders = []
    for idx, row in enumerate(qs, start=1):
        leaders.append({
            "rank": idx,
            "username": row["user__username"],
            "karma": row["karma"],
        })

    return Response({
        "window": "last_24_hours",
        "generated_at": timezone.now(),
        "leaders": leaders,
    })