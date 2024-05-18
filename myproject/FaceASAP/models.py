from django.db import models

class Video(models.Model):
    video_file = models.FileField(upload_to='videos/')
    face_encodings = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.video_file.name
