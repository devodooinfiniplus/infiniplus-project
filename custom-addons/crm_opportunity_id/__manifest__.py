{
    "name": "CRM Opportunity ID",
    "version": "18.0.1.0.0",
    "depends": [
        "crm",
        "vendor_qr_invoice",
        "sale_management",
        "fieldservice",
        "account",

    ],
    "author": "RSPlus",
    "data": [
        "data/sequence.xml",
        "views/vendor_qr_invoice_wizard_view.xml",
        "views/crm_lead_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "crm_opportunity_id/static/src/css/custom.css",
        ],
    },
    "installable": True,
    "application": True
}

