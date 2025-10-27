from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    request_vendor = fields.Many2one("res.partner", string="Request Vendor")
    no_kontrak = fields.Char("No Kontrak")
    with_po = fields.Boolean("With PO")
    purchase_order_ids = fields.One2many(
        "purchase.order", "sale_order_id", string="Purchase Orders"
    )

    def action_create_po(self):
        for order in self:
            if not order.request_vendor:
                raise ValidationError("Vendor tidak ditemukan. Harap pilih vendor terlebih dahulu.")
            
            po_vals = {
                "partner_id": order.request_vendor.id,
                "sale_order_id": order.id,
                "origin": order.name,
            }
            
            new_po = self.env["purchase.order"].create(po_vals)
            
            order.purchase_order_ids = [(4, new_po.id)]
            
            for line in order.order_line:
                if line.product_id:
                    po_line_vals = line._get_po_line_values(new_po.id, line.price_unit, line.product_uom_qty)
                    self.env["purchase.order.line"].create(po_line_vals)
        
        return True

    def action_confirm_so(self):
        for order in self:
            if order.no_kontrak:
                existing_orders = self.search([
                    ("no_kontrak", "=", order.no_kontrak),
                    ("id", "!=", order.id),
                    ("state", "!=", "cancel")
                ])
                
                if existing_orders:
                    raise ValidationError("No Kontrak sudah pernah diinputkan sebelumnya...!")
        
        return super(SaleOrder, self).action_confirm()

    def action_import_so_lines(self):
        return {
            "name": "Import SO Lines",
            "type": "ir.actions.act_window",
            "res_model": "import.so.lines.wizard",
            "view_mode": "form",
            "target": "new",
        }


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    sale_order_id = fields.Many2one("sale.order", string="Sales Order")


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_po_line_values(self, order, price, qty):
        return {
            "name": self.name,
            "product_id": self.product_id.id,
            "product_qty": qty or self.product_uom_qty,
            "product_uom": self.product_uom.id,
            "price_unit": price or self.price_unit,
            "order_id": order,
            "sale_line_id": self.id,
        }
