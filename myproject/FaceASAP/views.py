from django.shortcuts import render
from django.http import JsonResponse
import os
import face_recognition
import pickle
import uuid
from .models import FaceEncoding

def home(request):
    return render(request, 'index.html')

def upload_face_data(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        known_encodings = []
        for image in images:
            img = face_recognition.load_image_file(image)
            encodings = face_recognition.face_encodings(img)
            if encodings:
                known_encodings.append(encodings[0])

        if known_encodings:
            face_key = f'encodings_{uuid.uuid4().hex}.pickle'
            data = {"encodings": known_encodings}
            encodings_dir = os.path.join('media', 'encodings')
            os.makedirs(encodings_dir, exist_ok=True)
            encoding_file_path = os.path.join(encodings_dir, face_key)
            try:
                with open(encoding_file_path, 'wb') as f:
                    f.write(pickle.dumps(data))

                FaceEncoding.objects.create(face_key=face_key, file_path=encoding_file_path)
                return JsonResponse({'status': 'success', 'face_key': face_key})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        else:
            return JsonResponse({'status': 'error', 'message': 'No face encodings found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def upload_video_data(request):
    if request.method == 'POST':
        video_files = request.FILES.getlist('videos')
        video_paths = []
        videos_dir = os.path.join('media', 'videos')
        os.makedirs(videos_dir, exist_ok=True)
        for video_file in video_files:
            video_path = os.path.join(videos_dir, video_file.name)
            with open(video_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)
            video_paths.append(video_path)
        return JsonResponse({'status': 'success', 'video_paths': video_paths})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def get_uploaded_videos(request):
    media_dir = os.path.join('media', 'videos')
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)
    video_files = [os.path.join(media_dir, file) for file in os.listdir(media_dir) if file.endswith('.mp4')]
    return JsonResponse({'status': 'success', 'videos': video_files})

def search_videos(request):
    if request.method == 'POST':
        face_key = request.POST.get('face_key')
        if not face_key:
            return JsonResponse({'status': 'error', 'message': 'No face key provided'})

        encoding_file_path = os.path.join('media', 'encodings', face_key)
        with open(encoding_file_path, 'rb') as f:
            data = pickle.loads(f.read())
        
        known_encodings = data['encodings']
        tolerance = 0.6
        matched_videos = []

        for video_file in os.listdir('media/videos/'):
            if video_file.endswith('.mp4'):
                video_path = os.path.join('media', 'videos', video_file)
                video_capture = cv2.VideoCapture(video_path)
                frame_count = 0
                while True:
                    ret, frame = video_capture.read()
                    if not ret:
                        break
                    if frame_count % 30 == 0:
                        face_locations = face_recognition.face_locations(frame)
                        face_encodings = face_recognition.face_encodings(frame, face_locations)
                        for face_encoding in face_encodings:
                            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance)
                            if True in matches:
                                matched_videos.append(video_file)
                                break
                    frame_count += 1
                video_capture.release()
        return JsonResponse({'status': 'success', 'matched_videos': matched_videos})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
