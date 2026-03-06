from odoo import fields, models, _
from dateutil.relativedelta import relativedelta

from odoo.tools import format_date


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

    def _get_tax_closing_move_description(self, periodicity, period_start, period_end,
                                          fiscal_position):
        self.ensure_one()
        start = self.account_tax_periodicity_start_date

        if not start:
            return super()._get_tax_closing_move_description(periodicity, period_start, period_end,
                                                             fiscal_position)

        period_months = self._get_tax_periodicity_months_delay()

        # 1. Calculate total months elapsed since the very first start date
        total_diff_months = (period_start.year - start.year) * 12 + period_start.month - start.month

        # 2. Calculate the period number within a 12-month cycle
        # We use % 12 so that after 12 months, it restarts at Q1 or Month 1
        months_into_cycle = total_diff_months % 12
        period_number = (months_into_cycle // period_months) + 1

        # 3. Use the YEAR of the period_end.
        # For Dec 2025 - Feb 2026, this will correctly show 2026.
        display_year = period_end.year

        # 4. Region String (Standard)
        region_string = ''
        if self.env['account.fiscal.position'].search_count(
                [('company_id', '=', self.id), ('foreign_vat', '!=', False)]):
            fpos_country = fiscal_position.country_id.code if fiscal_position else self.account_fiscal_country_id.code
            region_string = f" ({fpos_country})"

        # 5. Formatted Strings
        if periodicity == 'year':
            return _("Tax return for %s%s", display_year, region_string)
        elif periodicity == 'trimester':
            return _("Tax return for Q%s %s%s", period_number, display_year, region_string)
        elif periodicity == 'monthly':
            return _("Tax return for Month %s %s%s", period_number, display_year, region_string)
        else:
            return _("Tax return from %s to %s%s", format_date(self.env, period_start),
                     format_date(self.env, period_end), region_string)