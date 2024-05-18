from django.contrib import admin
from django.urls import path, include
from FaceASAP import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('FaceASAP/', include('FaceASAP.urls')),
    path('', views.home, name='home'),
    path('upload/', views.upload_video, name='upload_video')
]
