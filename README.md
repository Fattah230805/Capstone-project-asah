# Capstone-project-asah

## AI-Powered Interview Assessment System

Repo ini berisi kode dan pipeline untuk proyek Capstone tim **A25-CS373** yang mengembangkan sistem otomatisasi penilaian wawancara berbasis AI. Sistem ini menganalisis video interview untuk menilai performa kandidat dan mendeteksi indikasi kecurangan seperti arah pandangan mata dan suara asing selama wawancara.

---

### Use Case:  
**DC-01 - AI-Powered Interview Assessment System**

---

### Tim:

- **Pradipta Rafa Taisir**  
- **Muhammad Fattah**  
- **Rafi Achmad Nabihan**

## Pipeline Usage Flow

Pipeline dijalankan secara berurutan melalui dua folder utama:

Pipeline_Feature_Extraction → Pipeline_Scoring_Video

1. **Pipeline_Feature_Extraction/**  
   Folder ini dijalankan terlebih dahulu.  
   - Input: video interview  
   - Output: file **CSV** berisi fitur hasil ekstraksi dari video

2. **Pipeline_Scoring_Video/**  
   Setelah CSV dihasilkan, lanjut ke folder ini.  
   - Input: file **CSV** dari Pipeline_Feature_Extraction  
   - Output: file **JSON** berisi hasil scoring interview menggunakan model yang telah dibuat
