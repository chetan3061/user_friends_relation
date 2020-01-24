from django.urls import path, include
from .views import FriendsDetailAPIView
app_name = 'friends_list'

urlpatterns = [
    path('friends', FriendsDetailAPIView.as_view(), name='friends_list'),
]