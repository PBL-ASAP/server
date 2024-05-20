import cv2
import face_recognition
import pickle
import uuid
import os

def get_face_encodings_from_video(video_path, sample_rate=30):
    face_encodings = []
    video_capture = cv2.VideoCapture(video_path)
    frame_count = 0
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        if frame_count % sample_rate == 0:
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
        if filename.endswith(".mp4"):
            video_path = os.path.join(directory, filename)
            video_face_encodings = get_face_encodings_from_video(video_path)
            for video_face_encoding in video_face_encodings:
                results = face_recognition.compare_faces([video_face_encoding], face_encodings, tolerance)
                if True in results:
                    matches.append(video_path)
                    break
    return matches

def generate_encodings_random_file(dataset_paths, names, number_images=10, image_type='.jpg', model_method='cnn'):
    knownEncodings = []
    knownNames = []

    for (i, dataset_path) in enumerate(dataset_paths):
        name = names[i]

        for idx in range(number_images):
            file_name = os.path.join(dataset_path, f"{idx + 1}{image_type}")

            image = cv2.imread(file_name)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            boxes = face_recognition.face_locations(rgb, model=model_method)
            encodings = face_recognition.face_encodings(rgb, boxes)

            for encoding in encodings:
                print(file_name, name, encoding)
                knownEncodings.append(encoding)
                knownNames.append(name)

    encoding_file = f'encodings_{uuid.uuid4().hex}.pickle'
    data = {"encodings": knownEncodings, "names": knownNames}
    with open(encoding_file, "wb") as f:
        f.write(pickle.dumps(data))

    return encoding_file

def detect_and_display(image, data, model_method='hog'):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model=model_method)
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"

        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)

        names.append(name)

    for ((top, right, bottom, left), name) in zip(boxes, names):
        y = top - 15 if top - 15 > 15 else top + 15
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        line = 2 if name != "Unknown" else 1

        cv2.rectangle(image, (left, top), (right, bottom), color, line)
        cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, line)
    return image
