from django.urls import path
from . import views

urlpatterns = [
    path('upload_face_data/', views.upload_face_data, name='upload_face_data'),
    path('upload_video_data/', views.upload_video_data, name='upload_video_data'),
    path('search_videos/', views.search_videos, name='search_videos'),
]
