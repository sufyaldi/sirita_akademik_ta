# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ThesisPromptExecution(models.Model):
    _name = 'thesis.prompt.execution'
    _description = 'Rekam Jejak & Audit Log Eksekusi Prompt AI'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    project_id = fields.Many2one(
        'thesis.project',
        string='Proyek Tugas Akhir',
        required=True,
        ondelete='cascade',
        index=True
    )
    student_id = fields.Many2one(
        related='project_id.student_id',
        string='Mahasiswa',
        store=True
    )
    prompt_id = fields.Many2one(
        'thesis.prompt.library',
        string='Template Prompt',
        required=True,
        index=True
    )
    prompt_code = fields.Char(related='prompt_id.code', string='Kode Prompt')
    name = fields.Char(
        string='Ringkasan Sesi',
        compute='_compute_name',
        store=True
    )

    compiled_prompt = fields.Text(
        string='Prompt Terkompilasi Lengkap',
        required=True,
        help='Prompt final yang dikirim ke sirita_ai_core termasuk parameter dan batasan etik'
    )
    ai_response = fields.Text(
        string='Respons GenAI',
        help='Hasil pemrosesan model LLM'
    )
    student_reflection = fields.Text(
        string='Refleksi Kritis Mahasiswa',
        help='Alasan mahasiswa memilih/menolak/memodifikasi rekomendasi AI'
    )

    state = fields.Selection([
        ('draft', 'Draf Input'),
        ('executed', 'Tereksekusi'),
        ('reviewed', 'Ditinjau Pembimbing'),
    ], string='Status', default='draft', tracking=True)

    @api.depends('prompt_id', 'create_date')
    def _compute_name(self):
        for rec in self:
            rec.name = f"[{rec.prompt_id.code or 'PROMPT'}] {rec.prompt_id.name or 'Sesi AI'}"

    def action_execute_ai(self):
        """Memanggil sirita_ai_core untuk memproses prompt akademik"""
        self.ensure_one()
        if not self.compiled_prompt:
            raise UserError(_("Prompt terkompilasi belum diisi!"))

        ai_service = self.env['ai.service']
        system_role = self.prompt_id.system_role or (
            "Anda adalah asisten metodologi penelitian akademik dan mitra dialektis. "
            "Bantu mahasiswa menajamkan pemikiran mereka tanpa mengambil alih kontrol intelektual. "
            "Patuhi batasan integritas ilmiah dan tolak fabrikasi atau halusinasi rujukan."
        )

        response = ai_service.ask_ai(
            prompt=self.compiled_prompt,
            system_instruction=system_role,
            response_format='text',
            temperature=0.3
        )

        self.write({
            'ai_response': response,
            'state': 'executed'
        })
        return True
