from rest_framework import serializers, viewsets
from .models import Follow , Reactions

class FollowSerializer(serializers.ModelSerializer):
     class Meta:
          model = Follow 
          fields = '__all__'

class ReactionSerializer(serializers.ModelSerializer):
     class Meta:
          model = Reactions
          fields = '__all__'