from .models import UserBlogPost , UserBlogComment
from rest_framework import serializers, viewsets


class UserBlogCommentSerialization(serializers.ModelSerializer):
     comment_by = serializers.ReadOnlyField(source = 'comment_by.id')
     class Meta:
          model = UserBlogComment
          fields = '__all__'
          
          def create(self, validated_data):
              return UserBlogComment.create(validated_data)

class UserBlogPostSerialization(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source = 'created_by.id')
    comments = UserBlogCommentSerialization(many=True, read_only=True)
    class Meta:
          model = UserBlogPost
          fields = ['id','created_by','title','description','status','created','modified','comments']

          def create(self, validated_data):
              return UserBlogPost.create(validated_data)
          
