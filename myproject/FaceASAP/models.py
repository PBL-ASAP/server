from django.db import models

class Video(models.Model):
    video_file = models.FileField(upload_to='videos/')
    face_encodings = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.video_file.name

class FaceEncoding(models.Model):
    face_key = models.CharField(max_length=64, unique=True)
    binary_data = models.BinaryField()

class VideoEncoding(models.Model):
    video_key = models.CharField(max_length=64, unique=True)
    binary_data = models.BinaryField()

class FaceEncoding(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    encoding_file = models.FileField(upload_to='encodings/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.encoding_file.name}"