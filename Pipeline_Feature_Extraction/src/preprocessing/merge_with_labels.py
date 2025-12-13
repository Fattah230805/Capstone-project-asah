import os
import pandas as pd

# Tentukan BASE_DIR otomatis dari lokasi script ini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folder data relatif ke project
DATA_DIR = os.path.join(BASE_DIR, "..", "..", "data")

# Path input/output
FEATURES_PATH = os.path.join(DATA_DIR, "audio_visual_features_final.csv")
LABELS_PATH   = os.path.join(DATA_DIR, "dataset_master", "labels.csv")
OUTPUT_PATH   = os.path.join(DATA_DIR, "dataset_features_labels.csv")

# Load CSV
features = pd.read_csv(FEATURES_PATH)
labels = pd.read_csv(LABELS_PATH)

# Merge fitur dengan label
merged = pd.merge(features, labels, on="video", how="inner")

# Simpan hasil
merged.to_csv(OUTPUT_PATH, index=False)

print("Merge selesai!")
print(f"File disimpan di: {OUTPUT_PATH}")
print("Jumlah baris:", merged.shape[0])
print("Jumlah kolom:", merged.shape[1])
print(merged.head())
