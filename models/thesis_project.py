# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ThesisProject(models.Model):
    _name = 'thesis.project'
    _description = 'Proyek Tugas Akhir Mahasiswa'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Judul Tugas Akhir / Skripsi', required=True, tracking=True)
    student_id = fields.Many2one(
        'res.users',
        string='Mahasiswa Peneliti',
        required=True,
        default=lambda self: self.env.user,
        tracking=True
    )
    advisor_ids = fields.Many2many(
        'res.users',
        'thesis_project_advisor_rel',
        'project_id',
        'advisor_id',
        string='Dosen Pembimbing',
        tracking=True
    )
    degree_level = fields.Selection([
        ('s1', 'Sarjana (S1)'),
        ('s2', 'Magister (S2)'),
        ('s3', 'Doktor (S3)'),
    ], string='Jenjang Studi', required=True, default='s1', tracking=True)

    stage_id = fields.Many2one(
        'thesis.stage',
        string='Tahapan Riset',
        group_expand='_read_group_stage_ids',
        tracking=True,
        index=True
    )

    research_topic = fields.Text(string='Bidang Minat / Topik Awal')
    research_questions = fields.Text(string='Rumusan Pertanyaan Penelitian')
    theoretical_framework = fields.Text(string='Kerangka Teori & Konsep')
    methodology_summary = fields.Text(string='Ringkasan Desain Metode')

    execution_ids = fields.One2many(
        'thesis.prompt.execution',
        'project_id',
        string='Riwayat Eksekusi AI'
    )
    execution_count = fields.Integer(
        string='Jumlah Eksekusi Prompt',
        compute='_compute_execution_count'
    )

    @api.depends('execution_ids')
    def _compute_execution_count(self):
        for rec in self:
            rec.execution_count = len(rec.execution_ids)

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        return self.env['thesis.stage'].search([])

    def action_launch_prompt_wizard(self):
        """Membuka wizard asisten prompt untuk proyek ini"""
        self.ensure_one()
        return {
            'name': 'Jalankan Asisten AI Riset Terbimbing',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.prompt.runner',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_project_id': self.id,
                'default_topic': self.research_topic or self.name,
                'default_theoretical_angle': self.theoretical_framework or False,
                'default_method_preference': self.methodology_summary or False,
            }
        }

    def action_view_executions(self):
        """Membuka daftar riwayat eksekusi AI untuk proyek ini"""
        self.ensure_one()
        return {
            'name': f'Audit Sesi AI: {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'thesis.prompt.execution',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }
