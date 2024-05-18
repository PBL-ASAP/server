from django.urls import path
from .views import home, upload_video

urlpatterns = [
    path('', home, name='home'),  # 기본 경로에 홈 뷰 연결
    path('upload/', upload_video, name='upload_video'),
]
