from django.shortcuts import render
from django.http import JsonResponse
from .utils import get_face_encodings_from_video, find_matching_videos
import os

def home(request):
    return JsonResponse({'message': 'Welcome to the Home Page'})

def upload_video(request):
    if request.method == 'POST':
        video_file = request.FILES.get('video')
        if video_file:
            video_path = os.path.join('media', video_file.name)
            with open(video_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)
            
            face_encodings = get_face_encodings_from_video(video_path)
            matched_videos = find_matching_videos('media', face_encodings)
            return JsonResponse({'status': 'success', 'matched_videos': matched_videos})
        return JsonResponse({'status': 'error', 'message': 'No video file provided'})
    elif request.method == 'GET':
        return JsonResponse({'message': 'Upload your video by POST request'}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
