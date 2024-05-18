from django.urls import path
from .views import upload_video, home

urlpatterns = [
    path('', home, name='home'),  # 루트 URL
    path('upload/', upload_video, name='upload_video'),  # 업로드 URL
]
