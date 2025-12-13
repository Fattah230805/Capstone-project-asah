import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import os

mp_face_mesh = mp.solutions.face_mesh

def euclidean(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

def head_movement(nose_prev, nose_now):
    if nose_prev is None:
        return 0
    return euclidean(nose_prev, nose_now)

def eye_aspect_ratio(eye):
    A = euclidean(eye[1], eye[5])
    B = euclidean(eye[2], eye[4])
    C = euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def gaze_direction(left_eye, right_eye):
    lx = left_eye[0][0]
    rx = right_eye[0][0]
    if lx < rx - 3:
        return "left"
    elif lx > rx + 3:
        return "right"
    return "center"

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    rows = []

    with mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1) as face_mesh:
        prev_nose = None
        blink_count = 0
        frame_id = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = face_mesh.process(rgb)

            if result.multi_face_landmarks:
                lm = result.multi_face_landmarks[0].landmark

                left_eye_idx = [33, 160, 158, 133, 153, 144]
                right_eye_idx = [362, 385, 387, 263, 373, 380]

                left_eye = [(lm[i].x * w, lm[i].y * h) for i in left_eye_idx]
                right_eye = [(lm[i].x * w, lm[i].y * h) for i in right_eye_idx]

                ear_left = eye_aspect_ratio(left_eye)
                ear_right = eye_aspect_ratio(right_eye)
                ear = (ear_left + ear_right) / 2

                blinking = 1 if ear < 0.21 else 0
                if blinking:
                    blink_count += 1

                nose = (lm[1].x * w, lm[1].y * h)
                movement = head_movement(prev_nose, nose)
                prev_nose = nose

                gaze = gaze_direction(left_eye, right_eye)

                rows.append({
                    "frame": frame_id,
                    "ear": ear,
                    "blink": blinking,
                    "head_movement": movement,
                    "gaze": gaze
                })

            frame_id += 1

    cap.release()
    return pd.DataFrame(rows)

def run_all():
    # Tentukan BASE_DIR otomatis dari lokasi script ini
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    input_folder = os.path.join(BASE_DIR, "..", "..", "data", "raw_videos")
    output_csv = os.path.join(BASE_DIR, "..", "..", "data", "visual_features.csv")

    all_rows = []
    for file in os.listdir(input_folder):
        if file.endswith((".mp4", ".webm", ".mov")):
            path = os.path.join(input_folder, file)
            df = process_video(path)
            df["video"] = file
            all_rows.append(df)

    if all_rows:
        final_df = pd.concat(all_rows, ignore_index=True)
        final_df.to_csv(output_csv, index=False)
        print("Saved:", output_csv)
    else:
        print("Tidak ada video ditemukan di folder:", input_folder)

if __name__ == "__main__":
    run_all()
