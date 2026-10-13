# -*- coding: utf-8 -*-
from odoo import models, fields

class ThesisPromptLibrary(models.Model):
    _name = 'thesis.prompt.library'
    _description = 'Pustaka Prompt Akademik Baku Tugas Akhir'
    _order = 'code, id'

    code = fields.Char(string='Kode Prompt', required=True, index=True)
    name = fields.Char(string='Nama / Aktivitas Prompt', required=True, index=True)
    appendix_source = fields.Selection([
        ('appendix_a', 'Lampiran A: Langkah 1 - Desain & Fondasi'),
        ('appendix_b', 'Lampiran B: Langkah 2 - Analisis & Data'),
        ('appendix_c', 'Lampiran C: Langkah 3 - Penulisan & Sintesis'),
        ('appendix_d', 'Lampiran D: Keterampilan GenAI Lanjutan'),
    ], string='Sumber Lampiran', required=True, default='appendix_a', index=True)

    target_degree = fields.Selection([
        ('s1', 'Sarjana (S1)'),
        ('s2_s3', 'Magister / Doktor (S2/S3)'),
        ('all', 'Semua Jenjang (S1 / S2 / S3)'),
    ], string='Target Jenjang Studi', required=True, default='all', index=True)

    system_role = fields.Text(
        string='Peran Instruksi Sistem (System Role)',
        help='Pedoman instruksi sistem untuk memposisikan AI sebagai rekan dialektis netral'
    )
    prompt_template = fields.Text(
        string='Template Instruksi Prompt',
        required=True,
        help='Teks prompt lengkap dengan placeholder variabel slot'
    )
    constraints = fields.Text(
        string='Batasan Akademik & Integritas',
        help='Klausul batasan metodologis, pencegahan halusinasi, dan etika'
    )
    output_target = fields.Text(
        string='Target Luaran Akademis',
        help='Kriteria hasil yang diharapkan untuk didiskusikan dengan pembimbing'
    )
    active = fields.Boolean(string='Aktif', default=True)
