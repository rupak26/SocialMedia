from django.db import models
from UserManagement.models import User
from contentManagement.models import UserBlogPost
# Create your models here.
class Follow(models.Model):
      follower = models.ForeignKey(User , related_name="following" , on_delete=models.CASCADE) 
      following = models.ForeignKey(User , related_name="followers" , on_delete=models.CASCADE)
      created_at = models.DateTimeField(auto_now_add=True)

      class Meta:
           unique_together = ('follower' , 'following')

class Reactions(models.Model):
      REACTION_CHOICES = [
            ('like' , 'Like') ,
            ('love' , 'Love') ,
            ('haha' , 'Haha') ,
            ('sad' ,  'Sad')  ,
            ('angry' , 'Angry')
      ]
      user = models.ForeignKey(User , on_delete=models.CASCADE)
      post = models.ForeignKey(UserBlogPost , on_delete=models.CASCADE , related_name="reactions")
      reaction_type = models.CharField(max_length=10,choices=REACTION_CHOICES)
      created_at = models.DateTimeField(auto_now_add=True)

      class Meta:
            unique_together = ('user' , 'post') 
