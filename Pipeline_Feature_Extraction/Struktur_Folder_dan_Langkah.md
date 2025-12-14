# Pipeline Feature Extraction

## Struktur Folder Project

⚠️ **Struktur folder HARUS sesuai** agar pipeline dapat berjalan dengan benar.  
Seluruh file `.py` **wajib diunduh** dan diletakkan sesuai struktur berikut:


Pipeline_Feature_Extraction/
│
├─ data/
│  ├─ raw_videos/
│  │  └─ video1.webm               # Video interview yang akan diekstrak fiturnya
│  ├─ dataset_master/
│  │  └─ labels.csv                # Label untuk training / manual scoring (opsional)
│  └─ processed/                   # Output dataset hasil ekstraksi fitur
│
├─ src/
│  └─ preprocessing/
│      ├─ analyze_audio.py         # Ekstraksi fitur audio
│      ├─ analyze_stt.py           # Speech-to-text (Whisper)
│      ├─ analyze_visual.py        # Ekstraksi fitur visual (MediaPipe)
│      ├─ aggregate_visual.py      # Agregasi fitur visual per video
│      ├─ merge_audio_visual.py    # Penggabungan fitur audio & visual
│      └─ merge_with_labels.py     # Penggabungan fitur dengan label (jika ada)
│
├─ pipeline_features.py            # Entry point pipeline
└─ requirements.txt                # Daftar dependensi Python

## Cara Menjalankan Pipeline Ekstraksi Fitur

### 1. Persyaratan Environment (Wajib)

Pipeline ini **dikembangkan dan diuji menggunakan environment berikut**:

- **Python 3.10.19**  
  Versi lain tidak direkomendasikan karena keterbatasan kompatibilitas **MediaPipe**.

- **FFmpeg (build 2025-12-04 – gyan.dev)**  
  Digunakan untuk ekstraksi audio dari video interview.

---

### 2. Install Dependensi Python

```bash
pip install -r requirements.txt

### 3. Menjalankan Pipeline
Jalankan perintah berikut dari folder Pipeline_Feature_Extraction:
python pipeline_features.py

### 4. Output
Pipeline akan memproses video di data/raw_videos/, ekstrak fitur, lalu simpan dataset final di data/processed/.
Dataset hasil ekstraksi siap digunakan untuk modelling atau testing selanjutnya.
