from odoo import http
from odoo.http import request,Response
import json

class ProcesosController(http.Controller):

    @http.route('/seguimiento_procesos', type='json', auth='public')
    def ordenes_trabajo(self, **kwargs):
        ordenes = request.env['dtm.proceso'].sudo().search([('status','!=','calidad'),('status','!=','terminado'),('status','!=','instalacion')])
        result = [{'orden':orden.ot_number,'status':orden.status,'tipo':orden.tipe_order,'cliente':orden.name_client,'producto':orden.product_name,'fecha_ini':orden.create_date,'po':orden.po_number,'fecha_rel':orden.date_rel} for orden in ordenes]
        return result

    @http.route('/seguimiento_materiales', type='http', auth='public')
    def lista_materiales(self, **kwargs):
        ordenes = request.env['dtm.proceso'].sudo().search(
            [('status', '!=', 'calidad'), ('status', '!=', 'terminado'), ('status', '!=', 'instalacion')])
        result = [
            {'orden': orden.ot_number, 'status': orden.status, 'tipo': orden.tipe_order, 'cliente': orden.name_client,
             'producto': orden.product_name, 'fecha_ini': orden.create_date, 'po': orden.po_number,
             'fecha_rel': orden.date_rel} for orden in ordenes]
        return request.make_response(
        json.dumps(result, default=str),
        headers=[('Content-Type', 'application/json')]
    )