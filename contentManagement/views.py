from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated , AllowAny
from .serializer import UserBlogPostSerialization ,UserBlogCommentSerialization
from .models import UserBlogPost,UserBlogComment,User 
from django.utils import timezone


class BlogPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = UserBlogPostSerialization(data=request.data)
            if serializer.is_valid():
                validate = dict(serializer.data)
                new_blogPost = UserBlogPost(
                    title = validate['title'] ,
                    description = validate['description'] ,
                    created_by = request.user
                )
                new_blogPost.save() 
                okay = UserBlogPostSerialization(new_blogPost)
                return Response(okay.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_204_NO_CONTENT)
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        try:
            created_by = request.user.id
            if created_by is not None:
                post = UserBlogPost.objects.filter(created_by = created_by)
                serializer = UserBlogPostSerialization(post,many = True)
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            return Response({'msg':'User Not Found'},status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request):
        try:
            post = UserBlogPost.objects.filter(
                id=request.query_params.get('post_id'),
                created_by=request.user.id
            ).last()
            if not post:
                return Response({'msg':'Permission Denied'},status=status.HTTP_404_NOT_FOUND)
            serializer = UserBlogPostSerialization(post,data=request.data)
            if not serializer.is_valid():
                return Response({'msg':'Invalid Data Surely'},status=status.HTTP_404_NOT_FOUND)
            serializer.save(modified = timezone.now())
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
    def patch(self, request):
        try: 
            id=request.query_params.get('id')
            created_by=request.user.id
        
            post = UserBlogPost.objects.filter(
                id = id,
                created_by = created_by).last()
            
            if post is None:
                return Response({'msg':'Invalid User'},status=status.HTTP_403_FORBIDDEN)
            
            serializer = UserBlogPostSerialization(post,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save(modified = timezone.now())
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    def delete(self, request):
        try:
            created_by = request.user.id
            id = request.query_params.get('id',None)
            post = UserBlogPost.objects.filter(
                created_by=created_by,
                id = id).last()
            if post is None:
                return Response({'msg' : 'Invalid User'},status=status.HTTP_403_FORBIDDEN)
        
            post.delete()
            return Response({'msg' : 'Content Deleted'},status=status.HTTP_200_OK)
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    

class BlogView(APIView):  
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            keyword = request.query_params.get('keyword',None)
            if keyword is not None:
                post = UserBlogPost.objects.filter(title__icontains=keyword) | UserBlogPost.objects.filter(description__icontains=keyword) | UserBlogPost.objects.filter(status__icontains=keyword)
                serializer = UserBlogPostSerialization(post, many=True)
                if not serializer.data:
                    return Response({'msg' : 'No related data'},status=status.HTTP_204_NO_CONTENT)
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                posts = UserBlogPost.objects.select_related('created_by').all()
                serializer = UserBlogPostSerialization(posts,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class BlogCommentView(APIView):
    permission_classes = [IsAuthenticated]
       
    def post(self,request):
        try:
            id = request.query_params.get('id')
            if id is not None:
                validate_data = dict(request.data)
                if not validate_data['body']:
                   return Response({'msg':'Empty comment can not be post'},status=status.HTTP_403_FORBIDDEN)
                new_blogcomment = UserBlogComment(
                        post = UserBlogPost(id) ,
                        comment_by = User(request.user.id) ,
                        body = validate_data['body'],
                )
                new_blogcomment.save()
                serializer = UserBlogCommentSerialization(new_blogcomment)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({'msg' : 'Post Id Not Found'},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
             return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
    
    def get(self,request):
         try:
            post_id = request.query_params.get('post_id')
            if post_id is not None:
                comment = UserBlogComment.objects.filter(post = post_id)
                serializer = UserBlogCommentSerialization(comment,many=True)
                if not serializer.data:
                    return Response({'msg' : 'This Post has No Comment'},status=status.HTTP_204_NO_CONTENT)
                
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'msg' : 'Post Id Not Found'},status=status.HTTP_401_UNAUTHORIZED)
         except Exception as error:
              return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    def put(self, request):
        try:
            id = request.query_params.get('id')
            if id:
                try:
                    comment = UserBlogComment.objects.get(id=id)
                except UserBlogComment.DoesNotExist:
                    return Response({'msg':'Not found any comment with this id'},status=status.HTTP_404_NOT_FOUND)
                
                serializer = UserBlogCommentSerialization(comment,data=request.data,partial=True)
                if not serializer.is_valid():
                    return Response({'msg':'Invalid Data Surely'},status=status.HTTP_404_NOT_FOUND)
                
                serializer.save(modified=timezone.now())
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'msg': 'Comment Id not Found'},status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request):
        try:
            id = request.query_params.get('id')
            if id:
                comment = UserBlogComment.objects.filter(id=id).first()
                if not comment:
                    return Response({'msg':'Not found any comment with this id'},status=status.HTTP_404_NOT_FOUND)
                
                serializer = UserBlogCommentSerialization(comment,data=request.data,partial=True)

                if not serializer.is_valid():
                   return Response({'msg':'Invalid Data'},status=status.HTTP_404_NOT_FOUND)
                
                serializer.save(modified=timezone.now())
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'msg' : 'Post Id Not Found'},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
     
    def delete(self, request):
        try:
            id = request.query_params.get('id')
            if id is not None:
                comment = UserBlogComment.objects.filter(id = id)

            if comment is None:
                return Response({'msg' : 'Invalid User'},status=status.HTTP_403_FORBIDDEN)
        
            comment.delete()
            return Response({'msg' : 'Content Deleted'},status=status.HTTP_200_OK)
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


## ONE SINGLE POST AND ALL ITS COMMENT 

class BlogPostCommentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request): 
        try:
            id = request.query_params.get('id')
            if id is not None:
                post = UserBlogPost.objects.filter(id = id)
                serializer = UserBlogPostSerialization(post,many = True)
                if not serializer.data:
                    return Response({'msg' : 'No Post Available With This ID'},status=status.HTTP_204_NO_CONTENT)
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            return Response({'msg':'User Not Found'},status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

