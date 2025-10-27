from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import ExcelExport
import io
import xlsxwriter


class ExcelDownloadController(http.Controller):

    @http.route("/web/binary/download_import_so_lines_template", type="http", auth="user")
    def download_import_so_lines_template(self, **kw):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet("SO Lines Template")
        
        # Header
        worksheet.write(0, 0, "Product Code")
        worksheet.write(0, 1, "Qty")
        worksheet.write(0, 2, "Unit Price")
        
        workbook.close()
        
        output.seek(0)
        file_content = output.read()
        
        return http.Response(
            file_content,
            headers=[
                ("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
                ("Content-Disposition", "attachment; filename=so_lines_template.xlsx;"),
                ("Content-Length", len(file_content))
            ]
        )