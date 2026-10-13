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
    prompt_name = fields.Char(related='prompt_id.name', string='Nama Aktivitas')
    appendix_source = fields.Selection(related='prompt_id.appendix_source', string='Tahapan Metodologi')
    target_degree = fields.Selection(related='prompt_id.target_degree', string='Target Jenjang')
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
    ai_response = fields.Html(
        string='Respons GenAI',
        help='Hasil pemrosesan model LLM (terformat kaya HTML)'
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

    is_cross_degree = fields.Boolean(
        string='Lintas Jenjang',
        compute='_compute_is_cross_degree',
        store=True,
        help='Menandai jika sesi AI menggunakan prompt di luar jenjang studi mahasiswa'
    )

    @api.depends('project_id.degree_level', 'prompt_id.target_degree')
    def _compute_is_cross_degree(self):
        for rec in self:
            if not rec.project_id or not rec.prompt_id or rec.prompt_id.target_degree == 'all':
                rec.is_cross_degree = False
            elif rec.project_id.degree_level == 's1' and rec.prompt_id.target_degree == 's2_s3':
                rec.is_cross_degree = True
            elif rec.project_id.degree_level in ['s2', 's3'] and rec.prompt_id.target_degree == 's1':
                rec.is_cross_degree = True
            else:
                rec.is_cross_degree = False

    @api.depends('prompt_id', 'create_date')
    def _compute_name(self):
        for rec in self:
            rec.name = f"[{rec.prompt_id.code or 'PROMPT'}] {rec.prompt_id.name or 'Sesi AI'}"

    @api.model
    def _markdown_to_html(self, text):
        """Konversi teks respons Markdown dari LLM menjadi Rich HTML yang rapi"""
        if not text:
            return ""
        if text.strip().startswith('<p>') or text.strip().startswith('<div>'):
            return text
        try:
            import markdown2
            return markdown2.markdown(
                text,
                extras=['fenced-code-blocks', 'tables', 'break-on-newline', 'cuddled-lists']
            )
        except Exception:
            try:
                import markdown
                return markdown.markdown(text, extensions=['extra', 'nl2br', 'sane_lists'])
            except Exception:
                import re
                html = text
                html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
                html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
                html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
                html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
                html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
                html = html.replace('\n', '<br/>')
                return html

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
        html_response = self._markdown_to_html(response)

        self.write({
            'ai_response': html_response,
            'state': 'executed'
        })
        return True

    def action_mark_reviewed(self):
        """Menandai sesi audit telah ditinjau dosen pembimbing"""
        self.ensure_one()
        self.write({'state': 'reviewed'})
        return True
