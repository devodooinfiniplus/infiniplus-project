{
    "name": "Vendor Invoice QR Code AT (Portugal)",
    "version": "18.0.2.1.0",
    "category": "Accounting",
    "summary": "Criar faturas de fornecedor através de QR Code da AT",
    "depends": ["account"],
    "author": "RSPlus",
    "data": [
        "security/ir.model.access.csv",
        "views/account_move_view.xml",
        "views/qr_invoice_wizard_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "vendor_qr_invoice/static/src/lib/jsQR.js",
            "vendor_qr_invoice/static/src/js/qr_scanner.js",
            "vendor_qr_invoice/static/src/xml/qr_scanner_templates.xml",
        ]
    },
    "installable": True,
    "application": False,
}
