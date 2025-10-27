{
    "name": "Custom Kurniawan",
    "version": "1.0",
    "depends": [
        "base",
        "sale",
        "purchase",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_view.xml",
        "wizard/import_so_lines_view.xml",
    ],
    "installable": True,
    "application": True,
    "external_dependencies": {
        "python": ["xlrd", "xlsxwriter"]
    }
}
