from django.urls import path
from .views import login_view, feed, me, post_comments, like_post, like_comment, leaderboard

urlpatterns = [
    path('login/', login_view),
    path('me/', me),
    path('feed/', feed),
    path('posts/<int:post_id>/comments/', post_comments),
    path('posts/<int:post_id>/like/', like_post),
    path('comments/<int:comment_id>/like/', like_comment),
    path('leaderboard/', leaderboard),

]