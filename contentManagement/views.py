from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken
from .serializer import userBlogPostSerialization 
from .models import userBlogComment , userBlogPost 
from UserManagement.models import User


class BlogPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = userBlogPostSerialization(data=request.data)
        if serializer.is_valid():
            validate = dict(serializer.data)
            newBlogPost = userBlogPost(title = validate['title'] , description = validate['description'] ,   created_by = User(request.user.id))
            newBlogPost.save() 
            okay = userBlogPostSerialization(newBlogPost)
            return Response(okay.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request):
        created_by = request.query_params.get('created_by',None)
        if created_by is not None:
            Targetobject = userBlogPost.objects.filter(created_by = created_by)
            serializer = userBlogPostSerialization(Targetobject,many = True)
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response({'msg':'User Not Found'},status=status.HTTP_404_NOT_FOUND)
        

    def put(self, request):
        id = request.query_params.get('created_by',None)
        if id is not None:
            Targetobject = userBlogPost.objects.get(id = id)
            serializer = userBlogPostSerialization(Targetobject,data=request.data)
            if serializer.is_valid():
               serializer.save()
               return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            return Response({'msg':'User Not Found'},status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request):
        id = request.query_params.get('id',None)
        if id is not None:
            Targetobject = userBlogPost.objects.filter(id = id)
            serializer = userBlogPostSerialization(Targetobject,data=request.data,Partial=True,many = True)
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response({'msg':'User Not Found'},status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request):
        id = request.query_params.get('id',None)
        if id is not None:
            Targetobject = userBlogPost.objects.filter(id = id)
            Targetobject.delete()
            return Response({'msg' : 'Content Deleted'},status=status.HTTP_200_OK)
        return Response({'msg':'User Not Found'},status=status.HTTP_404_NOT_FOUND)
