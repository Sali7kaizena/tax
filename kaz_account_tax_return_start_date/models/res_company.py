from odoo import fields, models
from dateutil.relativedelta import relativedelta


class ResCompany(models.Model):
    _inherit = 'res.company'

    account_tax_periodicity_start_date = fields.Date(string='Tax Return Start Date', company_dependent=True)

    def _get_tax_closing_period_boundaries(self, date):
        """ Returns the boundaries of the tax period containing the provided date,
        shifted by the account_tax_periodicity_start_date if set.
        """
        self.ensure_one()
        start_date = self.account_tax_periodicity_start_date
        if not start_date:
            return super()._get_tax_closing_period_boundaries(date)
            
        period_months = self._get_tax_periodicity_months_delay()
        
        # Calculate months difference between start_date and target date
        diff_months = (date.year - start_date.year) * 12 + date.month - start_date.month
        
        # Determine how many full periods have passed
        period_index = diff_months // period_months
        
        # Calculate the start of the current period relative to the custom start date
        p_start = start_date + relativedelta(months=period_index * period_months)
        p_end = p_start + relativedelta(months=period_months, days=-1)
        
        return p_start, p_end
