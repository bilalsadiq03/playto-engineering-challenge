from django.urls import path
from .views import feed, me

urlpatterns = [
    path('me/', me),
    path('feed/', feed),
]