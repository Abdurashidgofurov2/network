from django.urls import path
from .views import *

urlpatterns = [
    path('posts_create/', PostCreateAPIView.as_view()),
    path('posts/<str:uid>/details', PostDetailAPIView.as_view()),
    path('posts/<str:uid>/update/', PostUpdateAPIView.as_view()),
    path('posts/<str:uid>/delete/', PostDeleteAPIView.as_view()),
    path('myposts/', MyPostListAPIView.as_view()),
    path('myposts/', AllPostListAPIView.as_view()),
    path('files/', FileListView.as_view(), name='file-list'),
    path('upload_audio/', AudioFileUploadView.as_view(), name='upload-audio'),
    path('upload_video/', FileUploadView.as_view(), name='file-upload'),
    path('upload_image/', FileUploadView.as_view(), name='file-upload'),
    path('upload_other_files/', FileUploadView.as_view(), name='file-upload'),
]


