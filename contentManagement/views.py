from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated , AllowAny
from .serializer import UserBlogPostSerialization ,UserBlogCommentSerialization
from .models import UserBlogPost,UserBlogComment,User 
from django.utils import timezone
from rest_framework.pagination import LimitOffsetPagination

class BlogPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = UserBlogPostSerialization(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
            validate_data = dict(serializer.data)
            new_blogPost = UserBlogPost(
                title = validate_data['title'] ,
                description = validate_data['description'] ,
                created_by = request.user
            )
            new_blogPost.save() 
            postabledata = UserBlogPostSerialization(new_blogPost)    
            return Response(postabledata.data,status=status.HTTP_200_OK)  
        except Exception as error:
            return Response({
                'message' : 'Error on fetching',
                'Error' : error.__str__()
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        try:
            created_by = request.user.id
            post = UserBlogPost.objects.filter(
                created_by = created_by
            ).values()
            if not post:
                return Response({
                    'message':'User Not Found'}
                    ,status=status.HTTP_404_NOT_FOUND)
            
            return Response(post,status=status.HTTP_200_OK)
            
        except Exception as error:
            return Response({
                'message' : 'Error on fetching',
                'Error' : error.__str__()
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request):
        try:
            post = UserBlogPost.objects.filter(
                id=request.query_params.get('post_id'),
                created_by=request.user.id
            ).last()
            if not post:
                return Response({'msg':'User Does Not Matched'},status=status.HTTP_401_UNAUTHORIZED)
            serializer = UserBlogPostSerialization(post,data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
            
            serializer.save(modified = timezone.now())
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as error:
            return Response({
                'message' : 'Error on fetching',
                'Error' : error.__str__()
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
    def patch(self, request):
        try: 
            post_id=request.query_params.get('post_id')
            created_by=request.user.id
        
            post = UserBlogPost.objects.filter(
                id = post_id,
                created_by = created_by).last()
            if post is None:
                return Response({'msg':'User Does Not Matched'},status=status.HTTP_403_FORBIDDEN)
            
            serializer = UserBlogPostSerialization(post,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save(modified = timezone.now())
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
        except Exception as error:
            return Response({
                'message' : 'Error on fetching',
                'Error' : error.__str__()
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    def delete(self, request):
        try:
            created_by = request.user.id
            id = request.query_params.get('id',None)
            post = UserBlogPost.objects.filter(
                created_by=created_by,
                id = id).last()
            if post is None:
                return Response({'msg' : 'User Does Not Match'},status=status.HTTP_403_FORBIDDEN)
        
            post.delete()
            return Response({'msg' : 'Content Deleted'},status=status.HTTP_200_OK)
        except Exception as error:
            return Response({
                'message' : 'Error on fetching',
                'Error' : error.__str__()
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
# ALL POST WITH PROPER PAGINATION AND SEARCH 

class BlogView(APIView):  
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination
    def get(self, request):
        offset = int(request.query_params.get('offset',0))
        limit = int(request.query_params.get('limit',0))
        try:
            keyword = request.query_params.get('keyword',None)
            if keyword is not None:
                post = UserBlogPost.objects.filter(title__icontains=keyword) | UserBlogPost.objects.filter(description__icontains=keyword) | UserBlogPost.objects.filter(status__icontains=keyword)
                paginated_queryset = self.pagination_class().paginate_queryset(post, request)
                serializer = UserBlogPostSerialization(paginated_queryset, many=True)
                if not serializer.data:
                    return Response({'msg' : 'No related data'},status=status.HTTP_204_NO_CONTENT)
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                posts = UserBlogPost.objects.select_related('created_by').all()
                paginated_queryset = self.pagination_class().paginate_queryset(posts, request)
                serializer = UserBlogPostSerialization(paginated_queryset, many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as error:
            return Response({
                'message' : 'Error on fetching',
                'Error' : error.__str__()
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class BlogCommentView(APIView):
    permission_classes = [IsAuthenticated]
       
    def post(self,request):
        try:
            post_id = request.query_params.get('post_id')
            if post_id is not None:
                validate_data = dict(request.data)
                if not validate_data['body']:
                   return Response({'msg':'Empty comment can not be post'},status=status.HTTP_403_FORBIDDEN)
                new_blogcomment = UserBlogComment(
                        post = UserBlogPost(post_id) ,
                        comment_by = User(request.user.id) ,
                        body = validate_data['body'],
                )
                new_blogcomment.save()
                serializer = UserBlogCommentSerialization(new_blogcomment)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({'msg' : 'Post Id Not Found'},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as error:
             return Response({
                'message' : 'Error on fetching',
                'Error' : error.__str__()
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    
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
             return Response({
                'message' : 'Error on fetching',
                'Error' : error.__str__()
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    def put(self, request):
        try:
            comment_id = request.query_params.get('comment_id')
            if comment_id:
                try:
                    comment = UserBlogComment.objects.get(id=comment_id)
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
            return Response({
                'message' : 'Error on fetching',
                'Error' : error.__str__()
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request):
        try:
            comment_id = request.query_params.get('comment_id')
            if comment_id:
                comment = UserBlogComment.objects.filter(id=comment_id).first()
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
            return Response({
                'message' : 'Error on fetching',
                'Error' : error.__str__()
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
     
    def delete(self, request):
        try:
            comment_id = request.query_params.get('comment_id')
            if comment_id is not None:
                comment = UserBlogComment.objects.filter(id=comment_id)

            if comment is None:
                return Response({'msg' : 'User Does Not Matched'},status=status.HTTP_403_FORBIDDEN)
        
            comment.delete()
            return Response({'msg' : 'Content Deleted'},status=status.HTTP_200_OK)
        except Exception as error:
            return Response({
                'message' : 'Error on fetching',
                'Error' : error.__str__()
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)


## ONE SINGLE POST AND ALL ITS COMMENT 

class BlogPostCommentView(APIView):
    permission_classes = [AllowAny]
    def get(self, request): 
        try:
            post_id = request.query_params.get('post_id')
            if post_id is not None:
                post = UserBlogPost.objects.filter(id = post_id)
                serializer = UserBlogPostSerialization(post,many = True)
                if not serializer.data:
                    return Response(serializer.errors,status=status.HTTP_204_NO_CONTENT)
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            return Response({'msg' : 'No Post Available With This ID'},status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({
                'message' : 'Error on fetching',
                'Error' : error.__str__()
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
