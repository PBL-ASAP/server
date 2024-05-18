import cv2
import face_recognition
import numpy as np
import hashlib
import os

def get_face_encodings_from_video(video_path, sample_rate=30):
    face_encodings = []
    video_capture = cv2.VideoCapture(video_path)
    frame_count = 0

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        if frame_count % sample_rate == 0:  # 30프레임마다 한 번씩만 처리
            face_locations = face_recognition.face_locations(frame)
            for face_location in face_locations:
                face_encoding = face_recognition.face_encodings(frame, [face_location])[0]
                face_encodings.append(face_encoding)
        frame_count += 1

    video_capture.release()
    return face_encodings

def find_matching_videos(directory, face_encodings, tolerance=0.6):
    matches = []

    for filename in os.listdir(directory):
        if filename.endswith(('.mp4', '.mov', '.avi')):
            video_path = os.path.join(directory, filename)
            video_face_encodings = get_face_encodings_from_video(video_path)
            for face_encoding_to_match in face_encodings:
                for video_face_encoding in video_face_encodings:
                    results = face_recognition.compare_faces([video_face_encoding], face_encoding_to_match, tolerance)
                    if True in results:
                        matches.append(video_path)
                        break  # 이미 일치하는 비디오를 찾았으므로 다음 파일로 이동

    return matches

def hash_face_data(face_data):
    hash_object = hashlib.sha256()
    hash_object.update(np.array(face_data).tobytes())
    return hash_object.hexdigest()
