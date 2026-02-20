{
    'name': 'Accounting Tax Return Start Date',
    'version': '17.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Set a start date for tax periodicity to exclude old tax entries.',
    'description': """
Accounting Tax Return Start Date
================================
This module allows you to configure a start date for your tax periodicity.
It ensures that the tax report only includes entries from the active reporting period.

Key Features:
-------------
* Configure a "Tax Return Start Date" in Accounting Settings.
* Adds "Tax Period" and "Last Tax Period" filters to the Tax Report.
* Shifted periodicity logic: periods are calculated relative to the start date.
* Production ready for Kaizen Principles.
    """,
    'author': 'Kaizen Principles',
    'website': 'https://www.kaizenprinciples.ae',
    'depends': ['account', 'account_reports'],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'kaz_account_tax_return_start_date/static/src/xml/**/*.xml',
        ],
    },
    'images': ['static/description/icon.png'],
    'installable': True,
    'license': 'LGPL-3',
}
