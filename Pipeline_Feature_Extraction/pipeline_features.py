import os
import subprocess
import pandas as pd

# Tentukan BASE_DIR otomatis dari lokasi file ini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folder struktur dasar
RAW_VIDEOS = os.path.join(BASE_DIR, "data", "raw_videos")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
LABELS_PATH = os.path.join(BASE_DIR, "data", "dataset_master", "labels.csv")

# Folder script preprocessing
PREPROCESSING_DIR = os.path.join(BASE_DIR, "src", "preprocessing")


def run(script_name):
    """Menjalankan script preprocessing satu per satu."""
    script_path = os.path.join(PREPROCESSING_DIR, script_name)
    print(f"\nMenjalankan: {script_name}")

    try:
        subprocess.run(["python", script_path], check=True)
        print(f"Selesai: {script_name}")
    except subprocess.CalledProcessError:
        print(f"Terjadi error pada: {script_name}")
        raise


def main():
    print("Memulai pipeline preprocessing...\n")

    # Tahap utama ekstraksi fitur
    run("analyze_audio.py")
    run("analyze_stt.py")
    run("analyze_visual.py")
    run("aggregate_visual.py")
    run("merge_audio_visual.py")

    # Cek apakah labels.csv ada(buat training)
    if os.path.exists(LABELS_PATH):
        print("\nlabels.csv ditemukan. Menjalankan merge dengan labels...")
        run("merge_with_labels.py")
        final_dataset_path = os.path.join(BASE_DIR, "data", "dataset_features_labels.csv")
    else:
        print("\nlabels.csv tidak ditemukan. Lewati merge dengan labels.")
        final_dataset_path = os.path.join(PROCESSED_DIR, "audio_visual_features_final.csv")

    # Merge transcript 
    transcript_path = os.path.join(PROCESSED_DIR, "transcripts.csv")
    output_transcript_path = os.path.join(PROCESSED_DIR, "dataset_final_transcripts.csv")

    if os.path.exists(transcript_path):
        df_final = pd.read_csv(final_dataset_path)
        df_trans = pd.read_csv(transcript_path)

        # Normalisasi nama file untuk join
        df_final["file_id"] = df_final["video"].str.replace(r'\..*$', '', regex=True)
        df_trans["file_id"] = df_trans["audio"].str.replace(r'\..*$', '', regex=True)

        # Merge transcript ke dataset final
        merged = pd.merge(
            df_final,
            df_trans[["file_id", "transcript"]],
            on="file_id",
            how="inner"
        )

        merged.to_csv(output_transcript_path, index=False)
        print("transcripts.csv ditemukan. File dataset_with_transcripts.csv berhasil dibuat.")

    else:
        print("transcripts.csv tidak ditemukan. Lewati tahap merge transcript.")

    print("\nPipeline selesai dijalankan.")
    print("Semua output tersedia di folder: data/processed/")


if __name__ == "__main__":
    main()
