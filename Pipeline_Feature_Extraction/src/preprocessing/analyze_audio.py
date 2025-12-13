import os
import subprocess
import librosa
import numpy as np
import pandas as pd

# Tentukan BASE_DIR otomatis dari lokasi file ini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folder input & output relatif terhadap BASE_DIR
INPUT_DIR = os.path.join(BASE_DIR, "..", "..", "data", "raw_videos")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "data", "audio_outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

results = []

VIDEO_EXT = (".mp4", ".mov", ".webm", ".mkv", ".m4a", ".wav")

for file in os.listdir(INPUT_DIR):
    if file.lower().endswith(VIDEO_EXT):
        print(f"Processing: {file}")

        video_path = os.path.join(INPUT_DIR, file)
        base_name = os.path.splitext(file)[0]
        audio_path = os.path.join(OUTPUT_DIR, base_name + ".wav")

        # Ekstrak audio menggunakan ffmpeg
        subprocess.run([
            "ffmpeg", "-i", video_path,
            "-vn",          # tanpa video
            "-ac", "1",     # mono channel
            "-ar", "16000", # sampling rate 16kHz
            "-y", audio_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        try:
            y, sr = librosa.load(audio_path, sr=16000)

            zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)))
            energy = float(np.mean(y**2))
            mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1)
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

            result = {
                "filename": file,
                "zcr": zcr,
                "energy": energy,
                "tempo": float(tempo),
            }

            for i in range(len(mfcc)):
                result[f"mfcc_{i+1}"] = float(mfcc[i])

            results.append(result)

        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue

df = pd.DataFrame(results)
csv_path = os.path.join(OUTPUT_DIR, "audio_features.csv")
df.to_csv(csv_path, index=False)

print("\n=====================================")
print("FINISHED! Saved:", csv_path)
print("=====================================")
