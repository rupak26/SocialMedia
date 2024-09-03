from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated , AllowAny
from .serializer import userBlogPostSerialization , userParamSerialization ,userBlogCommentSerialization
from .models import userBlogPost,userBlogComment,User 
from datetime import datetime


class BlogPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = userBlogPostSerialization(data=request.data)
        if serializer.is_valid():
            validate = dict(serializer.data)
            new_blogPost = userBlogPost(
                title = validate['title'] ,
                description = validate['description'] ,
                created_by = request.user
            )
            new_blogPost.save() 
            okay = userBlogPostSerialization(new_blogPost)
            return Response(okay.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request):
        created_by = request.user.id
        if created_by is not None:
            post = userBlogPost.objects.filter(created_by = created_by)
            serializer = userBlogPostSerialization(post,many = True)
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response({'msg':'User Not Found'},status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request):
        post = userBlogPost.objects.filter(
            post_id=request.query_params.get('post_id'),
            created_by=request.user.id
        ).last()

        if not post:
            return Response({'msg':'Permission Denied'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = userBlogPostSerialization(post,data=request.data)
        if not serializer.is_valid():
            return Response({'msg':'Invalid Data'},status=status.HTTP_404_NOT_FOUND)
            
        serializer.save()
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
          
    def patch(self, request):
         
        id=request.query_params.get('id')
        created_by=request.user.id
      
        post = userBlogPost.objects.filter(
            id = id,
            created_by = created_by).last()
        
        if post is None:
            return Response({'msg':'Invalid User'},status=status.HTTP_403_FORBIDDEN)
        
        serializer = userBlogPostSerialization(post,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
 
    def delete(self, request):
        created_by = request.user.id
        id = request.query_params.get('id',None)
        post = userBlogPost.objects.filter(
            created_by=created_by,
            id = id).last()
        if post is None:
            return Response({'msg' : 'Invalid User'},status=status.HTTP_403_FORBIDDEN)
      
        post.delete()
        return Response({'msg' : 'Content Deleted'},status=status.HTTP_200_OK)
    
    

class BlogView(APIView):  
    permission_classes = [AllowAny]

    def get(self, request):
        keyword = request.query_params.get('keyword',None)
        if keyword is not None:
           post = userBlogPost.objects.filter(title__icontains=keyword) | userBlogPost.objects.filter(description__icontains=keyword)
           serializer = userParamSerialization(post, many=True)
           if not serializer.data:
               return Response({'msg' : 'No related data'},status=status.HTTP_204_NO_CONTENT)
           return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            posts = userBlogPost.objects.select_related('created_by').all()
            serializer = userBlogPostSerialization(posts,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        


class BlogCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
         id = request.query_params.get('id')
         if id is not None:
            validate = dict(request.data)
            new_blogcomment = userBlogComment(
                    body = validate['body'],
                    post = userBlogPost(id) ,
                    comment_by = User(request.user.id)
            )
            new_blogcomment.save()
            serializer = userBlogCommentSerialization(new_blogcomment)
            return Response(serializer.data,status=status.HTTP_200_OK)
         else:
            return Response({'msg' : 'Post Id Not Found'},status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        id = request.query_params.get('id')
        if id is not None:
            post = userBlogComment.objects.filter(id = id)
            if not post:
                 return Response({'msg':'Permission Denied'},status=status.HTTP_404_NOT_FOUND)
            
            serializer = userBlogCommentSerialization(post,data=request.data)

            if not serializer.is_valid():
               return Response({'msg':'Invalid Data'},status=status.HTTP_404_NOT_FOUND)
            
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'msg' : 'Post Id Not Found'},status=status.HTTP_401_UNAUTHORIZED)
    
    def patch(self, request):
        id = request.query_params.get('id')
        if id is not None:
            post = userBlogComment.objects.filter(id = id)
            if not post:
                 return Response({'msg':'Permission Denied'},status=status.HTTP_404_NOT_FOUND)
            
            serializer = userBlogCommentSerialization(post,data=request.data,partial=True)

            if not serializer.is_valid():
               return Response({'msg':'Invalid Data'},status=status.HTTP_404_NOT_FOUND)
            
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'msg' : 'Post Id Not Found'},status=status.HTTP_401_UNAUTHORIZED)
     
    def delete(self, request):
        id = request.query_params.get('id')
        if id is not None:
            comment = userBlogComment.objects.filter(id = id)

        if comment is None:
            return Response({'msg' : 'Invalid User'},status=status.HTTP_403_FORBIDDEN)
      
        comment.delete()
        return Response({'msg' : 'Content Deleted'},status=status.HTTP_200_OK)


## ONE SINGLE POST AND ALL ITS COMMENT 

class BlogPostCommentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request): 
        id = request.query_params.get('id')
        if id is not None:
            post = userBlogPost.objects.filter(id = id)
            serializer = userBlogPostSerialization(post,many = True)
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response({'msg':'User Not Found'},status=status.HTTP_404_NOT_FOUND)

