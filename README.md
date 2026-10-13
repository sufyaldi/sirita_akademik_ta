# SIRITA Akademik Tugas Akhir (`sirita_akademik_ta`)
### *Thesis Copilot & Mentoring Governance Platform for Odoo 20*

Modul Odoo 20 untuk tata kelola penelitian dan penulisan tugas akhir akademik (Skripsi S1, Tesis S2, Disertasi S3) yang mengintegrasikan metodologi **Model Tiga Langkah**, kemitraan reflektif kecerdasan buatan (GenAI), dan supervisi terstruktur dosen pembimbing.

---

## 🌟 Fitur Utama

1. **Pustaka 100+ Prompt Akademik Baku**:
   - **Lampiran A (40 Prompt)**: Fondasi & Desain Riset (Topik, Masalah, Hipotesis, Tinjauan Pustaka, Matriks Sumber, Kompatibilitas Teori, dan Desain Metodologis).
   - **Lampiran B (16 Prompt)**: Pengumpulan, Validasi Data, Ekstraksi Korpus, dan Analisis Empiris.
   - **Lampiran C (26 Prompt)**: Sintesis, Penulisan Naskah, Bab Pembahasan (*Discussion*), Rekonstruksi Pendahuluan, dan Poles Register Akademik.
   - **Lampiran D (18 Prompt)**: Keterampilan GenAI Lanjutan, Pertahanan Naskah Ujian Sidang, dan Format Interaksi Profesional Pembimbingan.

2. **Integrasi GenAI Terpusat via `sirita_ai_core`**:
   - Menggunakan layanan AI terpusat `self.env['ai.service'].ask_ai(...)`.
   - Mendukung model berkecepatan tinggi **Groq (Llama 3.3 70B, DeepSeek R1)** dan penalaran mendalam **Google Gemini 1.5 Pro/Flash**.
   - Dilengkapi penanganan fallback otomatis dan manajemen API Key terpusat.

3. **Wizard Asisten Riset Terbimbing (*Slot-Filling UI*)**:
   - Mahasiswa tidak perlu lagi merangkai prompt mentah.
   - Cukup memilih aktivitas riset dan mengisi parameter konteks (Topik, Alokasi Waktu, Akses Data, Kerangka Teori, Metode).
   - Pratinjau otomatis teks prompt beserta klausul batasan integritas akademik (*anti-hallucination* & *critical reasoning*).

4. **Pipeline Kanban Model Tiga Langkah**:
   - Memetakan progres penelitian secara visual dari tahap Desain $\rightarrow$ Analisis $\rightarrow$ Penulisan $\rightarrow$ Kesiapan Sidang Munaqasyah.

5. **Audit Trail & Refleksi Kritis Mahasiswa**:
   - Setiap interaksi prompt terekam secara otomatis.
   - Mahasiswa wajib mengisi lembar refleksi kritis (mengapa saran AI diterima, ditolak, atau dimodifikasi) yang dapat ditinjau oleh dosen pembimbing.

---

## 📂 Struktur Modul

```
sirita_akademik_ta/
├── __init__.py
├── __manifest__.py                  # Dependensi: base, mail, sirita_ai_core
├── .gitignore
├── README.md
├── data/
│   ├── thesis_stage_data.xml        # Tahapan Kanban Model Tiga Langkah
│   ├── prompt_library_lampiran_a.xml# 40 Prompt Desain & Fondasi
│   ├── prompt_library_lampiran_b.xml# 16 Prompt Analisis Data
│   ├── prompt_library_lampiran_c.xml# 26 Prompt Sintesis & Penulisan
│   └── prompt_library_lampiran_d.xml# 18 Prompt Keterampilan Lanjutan
├── models/
│   ├── __init__.py
│   ├── thesis_project.py            # Proyek Tugas Akhir & Tombol Aksi Wizard
│   ├── thesis_stage.py              # Tahapan Riset
│   ├── thesis_prompt_library.py     # Bank Data Prompt Akademik
│   └── thesis_prompt_execution.py   # Log Audit Eksekusi AI via sirita_ai_core
├── wizards/
│   ├── __init__.py
│   └── wizard_prompt_runner.py      # Wizard Penjalin Parameter Slot Prompt
├── views/
│   ├── menu_views.xml               # Menu Navigasi Modul
│   ├── thesis_project_views.xml     # Tampilan Kanban, Form & Smart Button
│   ├── thesis_prompt_library_views.xml # Katalog Pustaka Prompt
│   ├── thesis_prompt_execution_views.xml # Form Log Audit & Refleksi Mahasiswa
│   └── wizard_prompt_runner_views.xml # Popup Dialog Wizard Asisten Riset
└── security/
    ├── security_groups.xml          # Group: Mahasiswa, Dosen, Koordinator TA
    └── ir.model.access.csv          # Hak Akses Model
```

---

## 🚀 Prasyarat & Pemasangan

### Prasyarat
- **Odoo Versi 20.0**
- Modul dependensi: **`sirita_ai_core`** (wajib terpasang dan API Key Groq/Gemini telah dikonfigurasi).

### Langkah Pemasangan
1. Klon atau tempatkan repositori ini di dalam direktori addons Odoo Anda:
   ```bash
   git clone git@github.com:sufyaldi/sirita_akademik_ta.git
   ```
2. Pastikan `sirita_ai_core` berada di addons path yang sama.
3. Perbarui daftar modul Odoo (*Update Apps List*).
4. Cari modul **SIRITA Akademik Tugas Akhir** (`sirita_akademik_ta`) lalu klik **Install**.

---

## 👨‍💻 Pengembang

- **Author**: Sufyaldy | UPT TIPD IAIN Parepare
- **Website**: [https://iainpare.ac.id](https://iainpare.ac.id)
- **Lisensi**: LGPL-3
