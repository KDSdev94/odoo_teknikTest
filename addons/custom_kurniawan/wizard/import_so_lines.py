from odoo import models, fields, api
from odoo.exceptions import ValidationError
import base64
import xlrd


class ImportSoLinesWizard(models.TransientModel):
    _name = "import.so.lines.wizard"
    _description = "Import SO Lines Wizard"

    so_id = fields.Many2one("sale.order", string="Sales Order", default=lambda self: self.env.context.get('active_id'))
    import_file = fields.Binary(string="File Import", required=True)
    filename = fields.Char(string="File Name")

    def action_import_so_lines(self):
        if not self.import_file:
            raise ValidationError("Silakan pilih file untuk di-import.")
        
        file_content = base64.b64decode(self.import_file)
        
        workbook = xlrd.open_workbook(file_contents=file_content)
        worksheet = workbook.sheet_by_index(0)
        
        order = self.so_id
        
        for row_idx in range(1, worksheet.nrows):  # Mulai dari 1 untuk melewati header
            row = worksheet.row_values(row_idx)
            
            if len(row) < 3:
                continue  
            
            product_code = row[0]  
            qty = row[1]          
            unit_price = row[2]    
            
            if not product_code:
                continue  
            
            try:
                qty = float(qty) if qty else 0.0
                unit_price = float(unit_price) if unit_price else 0.0
            except ValueError:
                continue  
            
            product = self.env["product.product"].search([("default_code", "=", str(product_code))], limit=1)
            
            if not product:
                raise ValidationError(f"Produk dengan kode {product_code} tidak ditemukan.")
            
            self.env["sale.order.line"].create({
                "order_id": order.id,
                "product_id": product.id,
                "product_uom_qty": qty,
                "price_unit": unit_price,
            })
        
        # Refresh view
        return {
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "view_mode": "form",
            "res_id": order.id,
            "target": "current",
        }
    
    def action_download_template(self):
        return {
            "name": "Download Template Import SO Lines",
            "type": "ir.actions.act_url",
            "url": "/web/binary/download_import_so_lines_template",
            "target": "new",
        }
