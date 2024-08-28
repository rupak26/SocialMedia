from django.urls import path
from .views import BlogPost
urlpatterns = [
    path('create/',BlogPost.as_view(),name='BlogCreating')
]