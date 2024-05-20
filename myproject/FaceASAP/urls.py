from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_video, name='upload_video'),
    path('api/videos/', views.get_uploaded_videos, name='get_uploaded_videos'),
]
