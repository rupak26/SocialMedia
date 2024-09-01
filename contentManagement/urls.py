from django.urls import path
from .views import BlogPostCreation,BlogView
urlpatterns = [
    path('create/',BlogPostCreation.as_view(),name='BlogCreating'),
    path('view/',BlogView.as_view(),name='BlogView')
  #  path('comment/',)
]