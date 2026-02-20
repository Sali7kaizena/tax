from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    account_tax_periodicity_start_date = fields.Date(
        related='company_id.account_tax_periodicity_start_date',
        readonly=False,
        string="Tax Return Start Date",
    )
