from django.urls import path
from .views import BlogPost , BlogView ,BlogCommentView , BlogPostCommentView
urlpatterns = [
    path('post/',BlogPost.as_view(),name='BlogCreating'),
    path('view/',BlogView.as_view(),name='BlogView'),
    path('comment/',BlogCommentView.as_view(),name='BlogComment'),
    path('post/comment/',BlogPostCommentView.as_view(),name='BlogPostComment'),
]