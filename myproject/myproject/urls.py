from django.contrib import admin
from django.urls import path, include
from FaceASAP import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('upload_face_data/', views.upload_face_data, name='upload_face_data'),
    path('upload_video_data/', views.upload_video_data, name='upload_video_data'),
    path('api/videos/', views.get_uploaded_videos, name='get_uploaded_videos'),
    path('search_videos/', views.search_videos, name='search_videos'),
]
