from django.contrib import admin
from django.urls import path, include
from FaceASAP import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # 추가된 홈 페이지 URL
    path('upload_face_data/', views.upload_face_data, name='upload_face_data'),
    path('upload_video_data/', views.upload_video_data, name='upload_video_data'),
    path('api/videos/', views.get_uploaded_videos, name='get_uploaded_videos'),
    path('api/search_videos/', views.search_videos, name='search_videos'),  # 수정된 경로
]
