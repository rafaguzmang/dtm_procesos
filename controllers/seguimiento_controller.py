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
        # return request.make_response(
        # json.dumps(result, default=str),
        # headers=[('Content-Type', 'application/json')])

    @http.route('/seguimiento_materiales', type='json', auth='public')
    def lista_materiales(self, **kwargs):
        ordenes = request.env['dtm.proceso'].sudo().search(
            [('status', '!=', 'calidad'), ('status', '!=', 'terminado'), ('status', '!=', 'instalacion')])

        result = []

        for orden in ordenes:
            # Trae el ide de dtm_odt
            ot_id = request.env['dtm.odt'].sudo().search([('ot_number','=',orden.ot_number),('revision_ot','=',orden.revision_ot)])
            # lista_materiales = [f"{material.materials_list.id}: {material.nombre} {material.medida} - R - {material.materials_required} - {'compras' if material.revision else ''}" for material in ot_id.materials_ids]
            lista_materiales = [
                [
                    material.materials_list.id,
                    material.nombre,
                    material.medida,
                    material.materials_cuantity,
                    material.materials_required,
                    'Entregado' if request.env['dtm.materials.line'].search([('model_id', '=', ot_id.id)], limit=1).entregado else
                    'Comprado' if request.env['dtm.compras.realizado'].search([('orden_trabajo', '=', orden.ot_number), ('revision_ot', '=', orden.revision_ot),('codigo', '=', material.materials_list.id)], limit=1).comprado else
                    'En cámino' if request.env['dtm.compras.realizado'].search([('orden_trabajo','=',orden.ot_number),('revision_ot','=',orden.revision_ot),('codigo','=',material.materials_list.id)],limit=1) else
                    'En compra' if request.env['dtm.compras.requerido'].search([('orden_trabajo','=',orden.ot_number),('revision_ot','=',orden.revision_ot),('codigo','=',material.materials_list.id)],limit=1) else
                    'En Almacén' if request.env['dtm.materials.line'].search([('model_id','=',ot_id.id)],limit=1).materials_required == 0 and request.env['dtm.materials.line'].search([('model_id','=',ot_id.id)],limit=1).materials_cuantity > 0  else
                    'En Revisión' if not request.env['dtm.materials.line'].search([('model_id','=',ot_id.id)],limit=1) else
                    None
                ]
                for material in ot_id.materials_ids]
            lista_ordenada = sorted(lista_materiales,key=lambda item: item[5] in item)
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