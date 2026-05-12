
{
    "name": "Expense QR AT String",
    "version": "18.0.1.0.0",
    "category": "Expenses",
    "summary": "Scan QR AT and store string on expense",
    "depends": ["hr_expense"],
    "author": "RSPlus",
     "data": [
        "security/ir.model.access.csv",
        "views/hr_expense_views.xml",
        "views/qr_invoice_reader_wizard_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "expense_qr_string/static/src/lib/jsQR.js",
            "expense_qr_string/static/src/js/qr_scanner.js",
            "expense_qr_string/static/src/xml/templates.xml"
        ]
    },
    "installable": True,
    "application": True
}
