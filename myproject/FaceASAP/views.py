import os
from django.shortcuts import render
from django.http import JsonResponse
from .utils import get_face_encodings_from_video, find_matching_videos
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return JsonResponse({'message': 'Welcome to the Home Page'})


@csrf_exempt
def upload_video(request):
    # Your upload handling code
    if request.method == 'POST':
        video_files = request.FILES.getlist('videos')
        if video_files:
            video_paths = []
            
            # media 디렉토리가 없으면 생성
            if not os.path.exists('media'):
                os.makedirs('media')
                
            for video_file in video_files:
                video_path = os.path.join('media', video_file.name)
                
                with open(video_path, 'wb+') as destination:
                    for chunk in video_file.chunks():
                        destination.write(chunk)
                video_paths.append(video_file.name)
            
            return JsonResponse({'status': 'success', 'video_paths': video_paths})
        return JsonResponse({'status': 'error', 'message': 'No video file provided'})
    elif request.method == 'GET':
        return JsonResponse({'message': 'Upload your video by POST request'}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def get_uploaded_videos(request):
    media_dir = 'media'
    
    # media 디렉토리가 없으면 생성
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)

    video_files = []
    for file_name in os.listdir(media_dir):
        if file_name.endswith(".mp4") or file_name.endswith(".mov"):
            video_files.append(file_name)
    return JsonResponse({'video_files': video_files})
