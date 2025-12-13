import os
import glob
import pandas as pd
import whisper

# Tentukan BASE_DIR otomatis dari lokasi file ini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folder input & output relatif ke project
AUDIO_DIR = os.path.join(BASE_DIR, "..", "..", "data", "audio_outputs")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "..", "data", "processed")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    print("Loading Whisper model (medium)...")
    model = whisper.load_model("medium")

    audio_files = sorted(glob.glob(os.path.join(AUDIO_DIR, "*.wav")))
    print(f"Jumlah file audio ditemukan: {len(audio_files)}")

    if len(audio_files) == 0:
        print("Tidak ada file .wav di folder audio_outputs.")
        return

    transcripts = []

    for file in audio_files:
        fname = os.path.basename(file)
        print(f"\nTranscribing: {fname}")

        try:
            result = model.transcribe(file)
        except RuntimeError as e:
            print(f"Error (kemungkinan OOM). Menggunakan 'small' model sebagai fallback.")
            small_model = whisper.load_model("small")
            result = small_model.transcribe(file)

        transcripts.append({
            "audio": fname,
            "transcript": result["text"]
        })

    # Simpan hasil transcript
    out_path = os.path.join(OUTPUT_DIR, "transcripts.csv")
    pd.DataFrame(transcripts).to_csv(out_path, index=False)

    print("\nTranskripsi selesai!")
    print(f"File disimpan di: {out_path}")

if __name__ == "__main__":
    main()
