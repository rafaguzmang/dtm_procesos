from odoo import http
from odoo.http import request,Response
import json

class ProcesosController(http.Controller):

    @http.route('/seguimiento_procesos', type='json', auth='public')
    def ordenes_trabajo(self, **kwargs):
        ordenes = request.env['dtm.proceso'].sudo().search([('status','!=','calidad'),('status','!=','terminado'),('status','!=','instalacion')])
        result = [{
                    'orden':orden.ot_number,
                    'revision_ot':orden.revision_ot,
                    'status':orden.status,
                    'tipo':orden.tipe_order,
                    'cliente':orden.name_client,
                    'producto':orden.product_name,
                    'fecha_ini':orden.create_date,
                    'po':orden.po_number,
                    'fecha_rel':orden.date_rel
                } for orden in ordenes]
        return result

    @http.route('/seguimiento_materiales', type='json', auth='public')
    def lista_materiales(self, **kwargs):
        ordenes = request.env['dtm.proceso'].sudo().search(
            [('status', '!=', 'calidad'), ('status', '!=', 'terminado'), ('status', '!=', 'instalacion')])

        result = []

        for orden in ordenes:

            ot_id = request.env['dtm.odt'].sudo().search([('ot_number','=',orden.ot_number),('revision_ot','=',orden.revision_ot)])
            lista_materiales = [f"{material.materials_list.id}: {material.nombre} {material.medida} - R - {material.materials_required} - {'compras' if material.revision else ''}" for material in ot_id.materials_ids]
            lista_ordenada = sorted(lista_materiales,key=lambda item: 'compras' in item)
            result.append({
                'orden':orden.ot_number,
                'version':orden.revision_ot,
                'ot_id':ot_id.id,
                'materiales':lista_ordenada
            })

        return result
        # return request.make_response(
        # json.dumps(result, default=str),
        # headers=[('Content-Type', 'application/json')])