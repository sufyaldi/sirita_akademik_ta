# -*- coding: utf-8 -*-
from odoo import models, fields

class ThesisStage(models.Model):
    _name = 'thesis.stage'
    _description = 'Tahapan Pipeline Riset Tugas Akhir'
    _order = 'sequence, id'

    name = fields.Char(string='Nama Tahapan', required=True, translate=True)
    sequence = fields.Integer(string='Urutan', default=10)
    fold = fields.Boolean(string='Dilipat di Kanban', default=False)
    description = fields.Text(string='Deskripsi Tahap')
    step_category = fields.Selection([
        ('step1', 'Langkah 1: Fondasi dan Desain Riset'),
        ('step2', 'Langkah 2: Pengumpulan & Analisis Data'),
        ('step3', 'Langkah 3: Sintesis & Penulisan Naskah'),
        ('defense', 'Kesiapan Ujian Sidang / Munaqasyah'),
    ], string='Kategori Model Tiga Langkah', required=True, default='step1')
