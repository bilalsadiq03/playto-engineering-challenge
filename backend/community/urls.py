from django.urls import path
from .views import feed, me, post_comments, like_post, like_comment

urlpatterns = [
    path('me/', me),
    path('feed/', feed),
    path('posts/<int:post_id>/comments/', post_comments),
    path('posts/<int:post_id>/like/', like_post),
    path('comments/<int:comment_id>/like/', like_comment),

]