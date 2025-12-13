import os
import pandas as pd

# Tentukan BASE_DIR otomatis dari lokasi script ini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path input/output relatif ke project
AUDIO_PATH = os.path.join(BASE_DIR, "..", "..", "data", "audio_outputs", "audio_features.csv")
VISUAL_PATH = os.path.join(BASE_DIR, "..", "..", "data", "visual_features_aggregated.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "..", "data", "audio_visual_features_final.csv")

# Load CSV
audio_df = pd.read_csv(AUDIO_PATH)
visual_df = pd.read_csv(VISUAL_PATH)

# Rename kolom untuk merge
audio_df.rename(columns={"filename": "video"}, inplace=True)

# Pivot visual features untuk merge
visual_pivot = visual_df.pivot_table(
    index=[
        'video',
        'ear_mean', 'ear_min', 'ear_max',
        'blink_sum',
        'head_movement_mean', 'head_movement_min', 'head_movement_max'
    ],
    columns='level_1',
    values='gaze'
).reset_index()

# Pastikan kolom gaze prop terjaga
visual_pivot.rename(columns={
    'gaze_left_prop': 'gaze_left_prop',
    'gaze_right_prop': 'gaze_right_prop'
}, inplace=True)

# Merge audio dan visual
merged_df = pd.merge(audio_df, visual_pivot, on="video", how="inner")

# Simpan hasil
merged_df.to_csv(OUTPUT_PATH, index=False)

print("\nBERHASIL! Audio + Visual digabung tanpa error.")
print(f"File hasil: {OUTPUT_PATH}")
