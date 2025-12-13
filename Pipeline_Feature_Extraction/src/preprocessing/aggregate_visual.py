import os
import pandas as pd

# Tentukan BASE_DIR otomatis dari lokasi script ini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path file input/output relatif ke project
INPUT_CSV = os.path.join(BASE_DIR, "..", "..", "data", "visual_features.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "..", "..", "data", "visual_features_aggregated.csv")

# Baca data visual features
df = pd.read_csv(INPUT_CSV)

def gaze_proportion(gaze_series):
    total = len(gaze_series)
    left = (gaze_series == "left").sum()
    right = (gaze_series == "right").sum()
    return pd.Series({
        "gaze_left_prop": left / total,
        "gaze_right_prop": right / total
    })

# Hitung summary untuk ear, blink, head_movement
summary = df.groupby("video").agg({
    "ear": ["mean", "min", "max"],
    "blink": "sum",
    "head_movement": ["mean", "min", "max"]
}).reset_index()

summary.columns = ["_".join(col).strip("_") for col in summary.columns.values]

# Hitung proporsi gaze
gaze_summary = df.groupby("video")["gaze"].apply(gaze_proportion).reset_index()

# Merge summary dan gaze_summary
final_summary = pd.merge(summary, gaze_summary, on="video")

# Simpan hasil aggregated features
final_summary.to_csv(OUTPUT_CSV, index=False)
print("Visual features aggregated per video berhasil disimpan di:", OUTPUT_CSV)
