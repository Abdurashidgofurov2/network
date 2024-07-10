from django.db import models

from core import settings


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def file_url(self):
        # Assuming MEDIA_URL is '/media/'
        return f"{settings.MEDIA_URL}{self.file.name}"


