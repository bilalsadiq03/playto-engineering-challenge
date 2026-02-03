from django.urls import path
from .views import feed, me, post_comments

urlpatterns = [
    path('me/', me),
    path('feed/', feed),
    path('posts/<int:post_id>/comments/', post_comments),

]