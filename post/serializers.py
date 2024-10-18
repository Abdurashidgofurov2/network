
from rest_framework import serializers
from .models import *



class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = ['id', 'file', 'uploaded_at']



class UploadedFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = UploadedFile
        fields = ['id', 'file', 'uploaded_at', 'file_url']

    def get_file_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.file.url) if obj.file else None


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['uid', 'user', 'title', 'body', 'data_type', 'data', 'upload_time']
        read_only_fields = ['uid', 'user', 'upload_time']

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'body', 'data_type', 'data']

class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'body', 'data_type', 'data']
