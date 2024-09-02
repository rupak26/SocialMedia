from django.urls import path
from .views import BlogPost , BlogView , BlogSearch
urlpatterns = [
    path('create/',BlogPost.as_view(),name='BlogCreating'),
    path('view/',BlogView.as_view(),name='BlogView'),
    path('search/',BlogSearch.as_view(),name='BlogSearch'),
]