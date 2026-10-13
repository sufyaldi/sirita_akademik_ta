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
