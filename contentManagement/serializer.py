from .models import userBlogPost , userBlogComment
from rest_framework import serializers, viewsets


class userBlogCommentSerialization(serializers.ModelSerializer):
     class Meta:
          model = userBlogComment
          fields = '__all__'
     

class userBlogPostSerialization(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source = 'created_by.id')
    class Meta:
          model = userBlogPost
          fields = '__all__'

          def create(self, validated_data):
              return userBlogPost.create(validated_data)
          
class userParamSerialization(serializers.Serializer):
     title = serializers.CharField(required = False)
     description = serializers.CharField(required = False)