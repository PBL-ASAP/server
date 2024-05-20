from django.shortcuts import render
from django.http import JsonResponse
from .utils import get_face_encodings_from_video, find_matching_videos
from django.views.decorators.csrf import csrf_exempt
import os

def home(request):
    return JsonResponse({'message': 'Welcome to the Home Page'})
@csrf_exempt
def upload_video(request):
    if request.method == 'POST':
        video_files = request.FILES.getlist('videos')
        if video_files:
            video_paths = []
            for video_file in video_files:
                print(f"Uploading: {video_file.name}")  # 디버깅용 출력
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
    video_dir = os.path.join('media')
    videos = [f for f in os.listdir(video_dir) if os.path.isfile(os.path.join(video_dir, f))]
    return JsonResponse({'videos': videos})
