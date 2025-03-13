from django.shortcuts import render
from rest_framework import status 
from rest_framework.response import Response 
from rest_framework.views import APIView 
from .models import Follow , User , Reactions , UserBlogPost
from rest_framework.permissions import IsAuthenticated , AllowAny
# Create your views here.

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request , user_id):
        follower = request.user 
        try:
            following = User.objects.get(id=user_id)
            if follower != following:
                Follow.objects.get_or_create(
                    follower=follower,
                    following=following
                )
                return Response({"msg" : "Followed successfully"} , status=status.HTTP_201_CREATED)
            return Response({"msg" : "You can not follow yourself"} ,  status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error" : "User not found"} , status=status.HTTP_404_NOT_FOUND)
    
    def delete(self,request,user_id):
        follower = request.user
        try:
            following = User.objects.get(id=user_id)
            Follow.objects.filter(follower=follower,following=following).delete()
            return Response({"msg" : "Unfollowed successfully"},status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"msg" : "User not found"},status=status.HTTP_404_NOT_FOUND)


class ReactToPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request , post_id):
        user = request.user 
        reaction_type = request.query_params.get("reaction_type")

        if reaction_type not in dict(Reactions.REACTION_CHOICES):
            return Response({"error" : "Invalid reaction type"} ,status=status.HTTP_400_BAD_REQUEST)
        
        post = UserBlogPost.objects.get(id=post_id)
        created = Reactions.objects.update_or_create(
            user = user ,
            post = post ,
            defaults={"reaction_type" : reaction_type}
        )
        return Response({"msg" : "Reaction added" if created else "Reaction updated"} , status=status.HTTP_201_CREATED)

    def delete(self , request , post_id):
        user = request.user 
        Reactions.objects.filter(user=user , post_id=post_id).delete() 
        return Response({"msg" : "Reaction removed"} , status=status.HTTP_200_OK)
     

