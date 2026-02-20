from odoo import fields, models


class AccountReport(models.Model):
    _inherit = 'account.report'

    def _init_options_date(self, options, previous_options=None):
        super()._init_options_date(options, previous_options)
        
        # We only apply the default for tax-related reports.
        is_tax_report = self.env.ref('account_reports.tax_report', raise_if_not_found=False)
        if is_tax_report and (self == is_tax_report or self.root_report_id == is_tax_report):
            # If the filter is custom or today (default), force it to tax_period to match Odoo 18
            current_filter = options.get('date', {}).get('filter')
            if current_filter in ('custom', 'today') or not current_filter:
                date_from, date_to = self.env.company._get_tax_closing_period_boundaries(fields.Date.context_today(self))
                options['date'] = self._get_dates_period(date_from, date_to, 'range')
                options['date']['filter'] = 'tax_period'

    def _get_options_domain(self, options, date_scope):
        domain = super()._get_options_domain(options, date_scope)
        
        # We only apply the filter for tax-related reports.
        is_tax_report = self.env.ref('account_reports.tax_report', raise_if_not_found=False)
        
        if is_tax_report and (self == is_tax_report or self.root_report_id == is_tax_report):
            start_date = self.env.company.account_tax_periodicity_start_date
            if start_date:
                domain.append(('date', '>=', start_date))
        
        return domain
