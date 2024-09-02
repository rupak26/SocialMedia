from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated , AllowAny
from .serializer import userBlogPostSerialization , userParamSerialization
from .models import userBlogPost , User

class BlogPost(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = userBlogPostSerialization(data=request.data)
        if serializer.is_valid():
            validate = dict(serializer.data)
            newBlogPost = userBlogPost(
                title = validate['title'] ,
                description = validate['description'] ,
                created_by = request.user
            )
            newBlogPost.save() 
            okay = userBlogPostSerialization(newBlogPost)
            return Response(okay.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request):
        created_by = request.user.id
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
            serializer = userBlogPostSerialization(Targetobject,data=request.data,partial=True)
            if serializer.is_valid():
               serializer.save()
               return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response({'msg':'User Not Found'},status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request):
        created_by = request.user.id
        id = request.query_params.get('id',None)
        Targetobject = userBlogPost.objects.get(created_by=created_by,id = id)
        Targetobject.delete()
        return Response({'msg' : 'Content Deleted'},status=status.HTTP_200_OK)
    
    
    
class BlogSearch(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        keyword = request.query_params.get('keyword',None)
        print("===================")
        print(keyword)
        print("===================")
        if keyword is not None:
           posts = userBlogPost.objects.filter(title__icontains=keyword) | userBlogPost.objects.filter(description__icontains=keyword)
           serializer = userParamSerialization(posts, many=True)
           if serializer.data == []:
               return Response({'msg' : 'No related data'},status=status.HTTP_204_NO_CONTENT)
           return Response(serializer.data, status=status.HTTP_200_OK)
        #    for obj in serializer.data:
        #        if obj == validated_data:
        #            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'msg' : 'Not valid data'},status=status.HTTP_204_NO_CONTENT)
 

class BlogView(APIView):  
    permission_classes = [AllowAny]
    def get(self,request):
        posts = userBlogPost.objects.select_related('created_by').all()
        serializer = userBlogPostSerialization(posts,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    