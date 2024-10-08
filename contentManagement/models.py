from django.db import models
from UserManagement.models import User
from django.contrib.auth.base_user import AbstractBaseUser
# Create your models here.
# title, description, status:{published, draft}, created_by, created,modified

class UserBlogPost(models.Model):
      STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
      ]
      title = models.CharField(max_length=100)
      description = models.CharField(max_length=500)
      status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='draft')
      created_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name='posts')
      created = models.DateTimeField(auto_now_add=True)
      modified = models.DateTimeField(auto_now=True)

      def __str__(self):
            return self.title
      
class UserBlogComment(models.Model):
      post = models.ForeignKey(UserBlogPost, related_name='comments', on_delete=models.CASCADE)
      comment_by = models.ForeignKey(User,related_name='user_id',on_delete=models.CASCADE)
      body = models.TextField() 
      created = models.DateTimeField(auto_now_add=True)
      modified = models.DateTimeField(auto_now_add=True)
      
      def __str__(self):
            return self.body
