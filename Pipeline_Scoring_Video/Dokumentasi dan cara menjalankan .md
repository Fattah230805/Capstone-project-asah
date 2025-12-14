Berikut adalah dokumentasi lengkap dan panduan langkah demi langkah untuk menjalankan kode analisis video interview tersebut.

Kode ini dirancang khusus untuk berjalan di lingkungan **Google Colab** karena menggunakan fitur upload/download file bawaan Colab.

-----

# Dokumentasi Pipeline AI Analisis Interview

Sistem ini adalah pipeline otomatis yang menganalisis kandidat berdasarkan tiga modalitas: **Teks (Transcript)**, **Audio (Suara)**, dan **Visual (Gestur)**. Output akhirnya adalah file JSON yang berisi skor detail dan keputusan penerimaan.

## 1\. Persiapan Lingkungan (Environment)

Sebelum menjalankan kode, pastikan Anda menggunakan lingkungan yang mendukung.

  * **Platform:** Google Colab (Direkomendasikan).
  * **Library Tambahan:** Kode memerlukan library `sentence-transformers` yang mungkin perlu diinstal terlebih dahulu.

Tambahkan baris ini di sel paling atas notebook Anda jika belum ada:

```python
!pip install sentence-transformers pandas scikit-learn
```

## 2\. Persiapan Data Input (Format CSV)

Sistem ini **sangat sensitif** terhadap nama kolom di file CSV. Pastikan file CSV yang akan Anda upload memiliki kolom-kolom berikut:

### A. Identitas & Konten

  * `video`: Nama file video (contoh: `interview_q1.mp4`).
  * `transcript`: Teks jawaban kandidat (hasil Speech-to-Text).

### B. Fitur Audio (Diekstrak sebelumnya)

  * `tempo`: Kecepatan bicara.
  * `zcr`: Zero Crossing Rate.
  * `energy`: Energi suara/volume.
  * `mfcc_1` sampai `mfcc_13`: 13 kolom fitur MFCC untuk pengecekan kesamaan suara (deteksi kecurangan).

### C. Fitur Gestur (Diekstrak sebelumnya)

  * `ear_mean`, `ear_min`, `ear_max`: Eye Aspect Ratio (untuk deteksi fokus mata).
  * `blink_sum`: Jumlah kedipan.
  * `head_movement_mean`, `head_movement_min`, `head_movement_max`: Pergerakan kepala.
  * `gaze_left_prop`, `gaze_right_prop`: Proporsi arah pandangan mata.

-----

## 3\. Cara Menjalankan Pipeline

Ikuti langkah-langkah berikut untuk menghasilkan file JSON:

### Langkah 1: Jalankan Semua Sel Kode

Di Google Colab, klik menu **Runtime** \> **Run all** (atau tekan `Ctrl+F9`).
Notebook akan memuat model NLP (`all-mpnet-base-v2`). *Catatan: Proses ini mungkin memakan waktu 1-2 menit saat pertama kali dijalankan untuk mengunduh model.*

### Langkah 2: Proses Upload

Setelah kode sampai pada fungsi `process_interview_data()`, akan muncul tombol **"Choose Files"** atau prompt upload di bagian bawah notebook.

1.  Klik tombol tersebut.
2.  Pilih file CSV yang sudah Anda siapkan (sesuai format di poin 2).
3.  Tunggu proses upload selesai (0% -\> 100%).

### Langkah 3: Proses Analisis Otomatis

Setelah file terupload, sistem akan secara otomatis:

1.  **Analisis Teks:** Membandingkan transkrip kandidat dengan `ideal_answers` menggunakan *Semantic Similarity*.
2.  **Analisis Audio:** Menghitung skor kelancaran (*fluency*) dan mengecek apakah suara berubah drastis (indikasi joki/kecurangan).
3.  **Analisis Gestur:** Menilai fokus mata, kedipan, dan kestabilan kepala.
4.  **Penggabungan Skor:** Menghitung skor akhir berbobot.

### Langkah 4: Unduh Hasil JSON

Setelah selesai, notebook akan otomatis:

1.  Menampilkan hasil JSON di layar.
2.  Mengunduh file bernama `interview_results.json` ke komputer Anda.

-----

## 4\. Cara Membaca Hasil (JSON Structure)

File JSON yang dihasilkan akan memiliki struktur berikut untuk setiap video:

```json
[
    {
        "video": "nama_file_video.webm",
        "scores": {
            "text": 3,              // Skor Teks (0-4)
            "audio": 4,             // Skor Audio (0-4)
            "gesture": 2,           // Skor Gestur (0-4)
            "final_score": 6.75,    // Skor Akhir (Skala 1-10)
            "decision": "REVIEW_NEEDED" // Keputusan Sistem
        },
        "details": {
            "text": {
                "similarity": 0.58,
                "reason": "Jawaban cukup jelas..."
            },
            "audio": {
                "cheating_suspected": false // True jika suara terdeteksi beda orang
            },
            "gesture": {
                "anomaly_detected": false   // True jika gerakan mencurigakan
            }
        }
    }
]
```

## 5\. Logika Penilaian (Scoring Logic)

Untuk transparansi, berikut adalah bagaimana skor dihitung dalam kode ini:

**Bobot Penilaian:**

  * **Teks (Isi Jawaban):** 50%
  * **Audio (Kelancaran):** 30%
  * **Gestur (Sikap):** 20%

**Rumus:**
$$\text{Weighted} = (\text{Text} \times 0.5) + (\text{Audio} \times 0.3) + (\text{Gesture} \times 0.2)$$
$$\text{Final Score} = \text{Weighted} \times \frac{10}{4} \quad (\text{Konversi ke skala 10})$$

**Kriteria Keputusan:**

1.  **AI\_PASSED**: Skor $\ge$ 8.0
2.  **REVIEW\_NEEDED**: 5.0 $\le$ Skor \< 8.0
3.  **AI\_FAILED**: Skor \< 5.0

-----

## Tips Troubleshooting

1.  **Error "KeyError"**: Biasanya terjadi karena nama kolom di CSV tidak sama persis dengan yang diminta kode (misal `mfcc1` padahal kode minta `mfcc_1`). Periksa header CSV Anda.
2.  **Pertanyaan Tidak Sesuai**: Kode saat ini memiliki *hardcoded* kunci jawaban (`ideal_answers`) untuk pertanyaan ID 1 sampai 5. Pastikan urutan baris di CSV sesuai dengan urutan pertanyaan 1-5, atau sesuaikan dictionary `ideal_answers` di dalam kode jika pertanyaan Anda berbeda.