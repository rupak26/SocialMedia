from django.db import models
from UserManagement.models import User
from django.contrib.auth.base_user import AbstractBaseUser
# Create your models here.
#title, description, status:{published, draft}, created_by, created,modified

class userBlogPost(models.Model):
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
      
class userBlogComment(models.Model):
      post = models.ForeignKey(userBlogPost,related_name='comments',on_delete=models.CASCADE)
      user = models.CharField(max_length=100)
      content = models.TextField() 
      created = models.DateTimeField(auto_now_add=True)

      def __str__(self):
            return self.user