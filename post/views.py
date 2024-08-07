from django.shortcuts import render

from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .serializers import *
from .models import *


# class FileUploadView(generics.CreateAPIView):
#     queryset = UploadedFile.objects.all()
#     serializer_class = UploadedFileSerializer
#     parser_classes = (MultiPartParser, FormParser)
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#
# class FileListView(generics.ListAPIView):
#     queryset = UploadedFile.objects.all()
#     serializer_class = UploadedFileSerializer




class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer
    lookup_field = 'uid'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class PostDeleteAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    lookup_field = 'uid'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)




class MyPostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-upload_time')



class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'uid'
    permission_classes = [permissions.IsAuthenticated]