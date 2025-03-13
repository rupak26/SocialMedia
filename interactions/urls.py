from django.urls import path
from .views import FollowUserView , ReactToPostView

urlpatterns = [
    path('follow/<int:user_id>/',FollowUserView.as_view(),name='follow-user'),
    path('react/<int:post_id>/',ReactToPostView.as_view(),name='react-to-post'),
    #path('okokokokok/')
]