# -*- coding: utf-8 -*-
{
    'name': 'SIRITA Akademik Tugas Akhir (Thesis Copilot & Mentoring Governance)',
    'version': '20.0.1.0.0',
    'category': 'Academic/Thesis Management',
    'summary': 'Platform Pendampingan Riset & Pembimbingan Tugas Akhir Berbasis AI (Model Tiga Langkah)',
    'description': """
SIRITA Akademik Tugas Akhir (Thesis Copilot)
============================================
Modul tata kelola penelitian dan penulisan tugas akhir (Skripsi S1, Tesis S2, Disertasi S3)
yang mengintegrasikan kerangka metodologis ilmiah, kemitraan reflektif AI, dan supervisi
dosen pembimbing sesuai metodologi "Model Tiga Langkah".

Fitur Utama:
------------
* Pustaka 100+ Instruksi Prompt Akademik Baku (Lampiran A, B, C, D)
* Integrasi Layanan AI Terpusat via `sirita_ai_core` (Groq & Google Gemini)
* Wizard Interaktif Pengisian Parameter Riset (Slot-Filling UI)
* Audit Trail & Rekam Jejak Penggunaan AI Mahasiswa
* Pipeline Kanban Tahapan Riset (Desain -> Analisis -> Penulisan)
* Kolaborasi Dosen Pembimbing & Matriks Rencana Aksi Revisi (Tabel D.7)
* Pernyataan Pengungkapan AI Resmi (AI Disclosure Statement)
    """,
    'author': 'Sufyaldy | UPT TIPD IAIN Parepare',
    'website': 'https://iainpare.ac.id',
    'license': 'LGPL-3',
    'sequence': 10,
    'images': [
        'static/description/icon.png',
    ],
    'price': 0.0,
    'currency': 'USD',
    'depends': [
        'base',
        'mail',
        'sirita_ai_core',
    ],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'data/thesis_stage_data.xml',
        'data/prompt_library_lampiran_a.xml',
        'data/prompt_library_lampiran_b.xml',
        'data/prompt_library_lampiran_c.xml',
        'data/prompt_library_lampiran_d.xml',
        'views/wizard_prompt_runner_views.xml',
        'views/thesis_project_views.xml',
        'views/thesis_prompt_library_views.xml',
        'views/thesis_prompt_execution_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
