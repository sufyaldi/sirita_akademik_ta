# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import json

class WizardPromptRunner(models.TransientModel):
    _name = 'wizard.prompt.runner'
    _description = 'Wizard Peluncur Prompt Akademik Terbimbing'

    project_id = fields.Many2one(
        'thesis.project',
        string='Proyek Tugas Akhir',
        required=True
    )
    student_id = fields.Many2one(
        related='project_id.student_id',
        string='Mahasiswa Peneliti'
    )
    prompt_id = fields.Many2one(
        'thesis.prompt.library',
        string='Pilih Aktivitas Prompt',
        required=True
    )
    prompt_code = fields.Char(related='prompt_id.code', string='Kode Prompt')
    appendix_source = fields.Selection(related='prompt_id.appendix_source', string='Tahapan Sumber')
    target_degree = fields.Selection(related='prompt_id.target_degree', string='Jenjang Target')
    project_degree = fields.Selection(
        related='project_id.degree_level',
        string='Jenjang Proyek',
        readonly=True
    )
    filter_by_degree = fields.Boolean(
        string='Smart Filter (Khusus Jenjang Mahasiswa)',
        default=True,
        help='Membatasi pilihan aktivitas prompt hanya untuk jenjang studi mahasiswa saat ini'
    )
    is_degree_mismatch = fields.Boolean(
        string='Apakah Lintas Jenjang',
        compute='_compute_degree_mismatch'
    )
    mismatch_warning = fields.Text(
        string='Pesan Peringatan Jenjang',
        compute='_compute_degree_mismatch'
    )

    # Parameter Slot Inputs (Slot-filling form)
    topic = fields.Char(
        string='Topik / Bidang Minat',
        help='Contoh: Evaluasi Kinerja Algoritma Klasifikasi Teks pada Media Sosial'
    )
    available_time = fields.Char(
        string='Alokasi Waktu yang Tersedia',
        default='4-6 Bulan',
        help='Contoh: 1 Semester (6 Bulan) atau 3 Bulan'
    )
    data_access = fields.Text(
        string='Data / Korpus yang Dapat Diakses',
        help='Contoh: 5000 data cuitan Twitter API publik atau transkrip 15 wawancara informan'
    )
    theoretical_angle = fields.Char(
        string='Sudut Pandang Teoretis / Konsep',
        help='Contoh: Teori Difusi Inovasi Rogers atau Kerangka TAM'
    )
    method_preference = fields.Char(
        string='Preferensi Metode / Pendekatan',
        help='Contoh: Kualitatif Studi Kasus / Kuantitatif SEM-PLS'
    )
    additional_notes = fields.Text(
        string='Catatan Tambahan / Konteks Lapangan',
        help='Kondisi khusus atau batasan objek penelitian'
    )

    # Preview & Output
    preview_prompt = fields.Text(
        string='Pratinjau Prompt Terkompilasi',
        readonly=True
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        project_id = res.get('project_id') or self.env.context.get('default_project_id')
        if project_id:
            project = self.env['thesis.project'].browse(project_id)
            if not res.get('topic') and project.research_topic:
                res['topic'] = project.research_topic
            if not res.get('theoretical_angle') and project.theoretical_framework:
                res['theoretical_angle'] = project.theoretical_framework
            if not res.get('method_preference') and project.methodology_summary:
                res['method_preference'] = project.methodology_summary
        return res

    @api.depends('project_id.degree_level', 'prompt_id.target_degree')
    def _compute_degree_mismatch(self):
        for rec in self:
            if not rec.project_id or not rec.prompt_id or rec.prompt_id.target_degree == 'all':
                rec.is_degree_mismatch = False
                rec.mismatch_warning = ""
            elif rec.project_id.degree_level == 's1' and rec.prompt_id.target_degree == 's2_s3':
                rec.is_degree_mismatch = True
                rec.mismatch_warning = (
                    f"⚠️ PERINGATAN PEDAGOGIS: Aktivitas [{rec.prompt_id.code}] dirancang khusus untuk jenjang "
                    f"Magister / Pascasarjana (S2/S3). Mahasiswa peneliti terdaftar pada jenjang Sarjana (S1). "
                    f"Tuntutan kontribusi teoretis, sintesis mutakhir, dan kebaruan pada prompt ini "
                    f"berada di atas standar skripsi S1. Disarankan memilih kode A.4.1.1 (Sarjana S1) "
                    f"atau memastikan telah disetujui Dosen Pembimbing."
                )
            elif rec.project_id.degree_level in ['s2', 's3'] and rec.prompt_id.target_degree == 's1':
                rec.is_degree_mismatch = True
                rec.mismatch_warning = (
                    f"ℹ️ CATATAN METODOLOGI: Aktivitas [{rec.prompt_id.code}] adalah standar Sarjana (S1). "
                    f"Untuk jenjang Pascasarjana ({rec.project_id.degree_level.upper()}), disarankan "
                    f"menggunakan aktivitas berorientasi kontribusi teoretis tingkat lanjut."
                )
            else:
                rec.is_degree_mismatch = False
                rec.mismatch_warning = ""

    @api.onchange('project_id', 'filter_by_degree')
    def _onchange_project_id_filter(self):
        domain = []
        if self.project_id and self.filter_by_degree:
            if self.project_id.degree_level == 's1':
                domain = [('target_degree', 'in', ['s1', 'all'])]
            else:
                domain = [('target_degree', 'in', ['s2_s3', 'all'])]
            if self.prompt_id and self.prompt_id.target_degree not in (['s1', 'all'] if self.project_id.degree_level == 's1' else ['s2_s3', 'all']):
                self.prompt_id = False
        return {'domain': {'prompt_id': domain}}

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id:
            if not self.topic and self.project_id.research_topic:
                self.topic = self.project_id.research_topic
            if not self.theoretical_angle and self.project_id.theoretical_framework:
                self.theoretical_angle = self.project_id.theoretical_framework
            if not self.method_preference and self.project_id.methodology_summary:
                self.method_preference = self.project_id.methodology_summary

    @api.onchange('prompt_id', 'topic', 'available_time', 'data_access', 'theoretical_angle', 'method_preference', 'additional_notes')
    def _onchange_compile_preview(self):
        for rec in self:
            if rec.prompt_id:
                rec.preview_prompt = rec._build_compiled_prompt()
            else:
                rec.preview_prompt = ""

    def _build_compiled_prompt(self):
        """Menyusun teks prompt baku dari template dan input variabel mahasiswa"""
        self.ensure_one()
        p = self.prompt_id
        content_lines = []

        content_lines.append(f"Aktivitas: [{p.code}] {p.name}")
        content_lines.append("--------------------------------------------------")
        content_lines.append("KONTEKS & VARIABEL PENELITI:")
        if self.topic:
            content_lines.append(f"- Topik Awal/Minat: {self.topic}")
        if self.available_time:
            content_lines.append(f"- Alokasi Waktu: {self.available_time}")
        if self.data_access:
            content_lines.append(f"- Akses Data/Materi: {self.data_access}")
        if self.theoretical_angle:
            content_lines.append(f"- Orientasi Teoretis: {self.theoretical_angle}")
        if self.method_preference:
            content_lines.append(f"- Pendekatan/Metode: {self.method_preference}")
        if self.additional_notes:
            content_lines.append(f"- Catatan Khusus: {self.additional_notes}")

        content_lines.append("\nPANDUAN INSTRUKSI TUGAS:")
        content_lines.append(p.prompt_template or "")

        if p.constraints:
            content_lines.append("\nBATASAN AKADEMIK & INTEGRITAS:")
            content_lines.append(p.constraints)

        if p.output_target:
            content_lines.append("\nTARGET LUARAN YANG DIHARAPKAN:")
            content_lines.append(p.output_target)

        return "\n".join(content_lines)

    def action_generate_and_execute(self):
        """Kompilasi prompt, eksekusi via sirita_ai_core, dan simpan log audit"""
        self.ensure_one()
        if not self.prompt_id:
            raise UserError(_("Pilih salah satu template prompt terlebih dahulu!"))

        compiled = self._build_compiled_prompt()

        # Buat rekam jejak eksekusi
        execution = self.env['thesis.prompt.execution'].create({
            'project_id': self.project_id.id,
            'prompt_id': self.prompt_id.id,
            'compiled_prompt': compiled,
            'state': 'draft'
        })

        # Panggil sirita_ai_core secara instan
        execution.action_execute_ai()

        # Buka langsung form audit log hasil eksekusi
        return {
            'name': _('Hasil Sesi AI Akademik'),
            'type': 'ir.actions.act_window',
            'res_model': 'thesis.prompt.execution',
            'res_id': execution.id,
            'view_mode': 'form',
            'target': 'current',
        }
