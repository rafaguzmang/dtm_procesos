from odoo import http
from odoo.http import request,Response
import json
from datetime import datetime
class ProcesosController(http.Controller):
    # Carga las ordenes de trabajo y su estado en los procesos
    @http.route('/seguimiento_procesos', type='http', auth='public')
    def ordenes_trabajo(self, **kwargs):
        # Se obtienen todas las ordenes de trabajo
        ordenes_trabajo = request.env['dtm.odt'].sudo().search([])
        result = []
        for orden in ordenes_trabajo:
            procesos_id = request.env['dtm.proceso'].sudo().search([('ot_number','=',orden.ot_number),('revision_ot','=',orden.revision_ot)],limit=1)
            # Status del corte
            corte_id = request.env['dtm.materiales.laser'].sudo().search([('orden_trabajo','=',orden.ot_number),('revision_ot','=',orden.revision_ot)])
            corte_finalizado_id = request.env['dtm.laser.realizados'].sudo().search([('orden_trabajo','=',orden.ot_number),('revision_ot','=',orden.revision_ot)])
            corte = "N/A"
            if corte_finalizado_id and not corte_id:
                corte = "100%"
            if corte_id:
                corte = f"{round(corte_id.status, 2)}%" 

            # Status de maquinado
            maquinados_id = request.env['dtm.maquinados'].sudo().search([('orden_trabajo','=',orden.ot_number),('revision_ot','=',orden.revision_ot)])
            maquinados_finalizado_id = request.env['dtm.maquinados.terminados'].sudo().search([('orden_trabajo','=',orden.ot_number),('revision_ot','=',orden.revision_ot)])
            maquinado = "N/A"
            if maquinados_finalizado_id and not maquinados_id:
                maquinado = "100%"
            if maquinados_id:
                maquinado = f"{round(maquinados_id.status,2)}%"

            # Status del material en compras
            get_requerido = request.env['dtm.compras.requerido'].sudo().search([('orden_trabajo','=',orden.ot_number),('revision_ot','=',orden.revision_ot)])
            get_realizado = request.env['dtm.compras.realizado'].sudo().search([('orden_trabajo','=',orden.ot_number),('revision_ot','=',orden.revision_ot),('listo_btn','!=',True)])
            requerido = len(get_requerido.ids) if get_requerido else 0
            realizado = len(get_realizado.ids) if get_realizado else 0
            vals = {
                    'orden':orden.ot_number,
                    'version_ot':orden.revision_ot,
                    'tipo':orden.tipe_order,
                    'cliente':orden.name_client,
                    'producto':orden.product_name,
                    'fecha_entrega':orden.date_rel.strftime("%x"),
                    'nesteo':'100%' if orden.firma_ingenieria else '0%',
                    'compra_material':f"{procesos_id.materials}%",
                    'corte': corte,
                    'maquinado': maquinado,
                    'habilitado':'',
                    'ensamble':'',
                    'soldadura':'',
                    'limpieza':'',
                    'tipo_acabado':'',
                    'acabado':'',
                    'cotizacion':orden.no_cotizacion,
                    'terminado':'Terminado' if procesos_id.status == 'terminado' else '',
                    'po':orden.po_number,
                    'prioridad':orden.prioridad,
                    'requerido':requerido,
                    'realizado':realizado,
            }
            result.append(vals)
        # datetime.strptime(x["fecha"], "%d/%m/%Y")
        result = sorted(result,key=lambda x:datetime.strptime(x["fecha_entrega"], "%d/%m/%Y"))
        return request.make_response(
                json.dumps(result),
                    headers={
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin':'*'
                    }
                )
    # Carga los materiales de una orden de trabajo y su estado
    @http.route('/seguimiento_materiales', type='json', auth='public')
    def lista_materiales(self, **kwargs):
        raw = request.httprequest.data
        data = json.loads(raw)
        orden = data.get('orden')
        revision = data.get('version')
        ordenes = request.env['dtm.odt'].sudo().search([('ot_number','=',orden),('revision_ot','=',revision)],limit=1)

        result = []
        for material in ordenes.materials_ids:
            cotizaciones = request.env['dtm.compras.requerido'].search([('orden_trabajo', '=', orden), ('revision_ot', '=', revision),
                                                                        ('codigo', '=', material.materials_list.id)], limit=1)
            compras = request.env['dtm.compras.realizado'].search([ ('orden_trabajo', '=', orden), ('revision_ot', '=', revision),
                                                                    ('codigo', '=', material.materials_list.id)], limit=1)
            result.append({

                "id": material.materials_list.id,
                "nombre": material.nombre,
                "medida": material.medida,
                "cantidad_solicitada": material.materials_cuantity,
                "cantidad_disponible": material.materials_availabe,
                "status":   'Entregado' if material.entregado else
                            'Recibido por Almacén' if compras.comprado == 'Recibido' else
                            'Comprado' if compras.listo_btn and compras.comprado != 'Recibido' else
                            'En Cotizaciones' if cotizaciones else
                            'En Almacén' if not material.revision and material.almacen else
                            'En Revisión' if not material.almacen else None
            })

            result = sorted(result, key=lambda x: x["status"] == 'Entregado')

        
       
        return result
       
    # Carga los cortes y sus estados
    @http.route('/seguimiento_corte_laser', type='json', auth='public')
    def lista_cortes(self):
        raw = request.httprequest.data
        data = json.loads(raw)
        orden = data.get('orden')
        revision = data.get('version')
        # Buscamos los cortes asociados a la orden de trabajo
        orden_id = request.env['dtm.odt'].sudo().search([('ot_number','=',orden),('revision_ot','=',revision)],limit=1)
        result = []
        if orden_id.primera_pieza_id:
            for primera in orden_id.primera_pieza_id:
                # Se busca por nombre del archivo y se compara si está asociado a la orden tanto en archivo en corte como en terminado
                en_corte_id = request.env['dtm.documentos.cortadora'].sudo().search([('nombre','=',primera.nombre)])
                filtro_model_id = en_corte_id.filtered(lambda record: record.model_id.orden_trabajo == orden and record.model_id.revision_ot ==revision)
                finalizado_id = request.env['dtm.documentos.finalizados'].sudo().search([('nombre','=',primera.nombre)])
                filtro_finalizado_id = finalizado_id.filtered(lambda  record:record.model_id.orden_trabajo == orden and record.model_id.revision_ot == revision)
                # Si está en finalizado el porcentaje está en 100 y si no se pone el porcentaje real del corte
                if filtro_finalizado_id:
                    porcentaje = '100%'
                    tiempo_total = round(sum(filtro_finalizado_id.tiempos_id.mapped("tiempo")),2)
                elif filtro_model_id:
                    porcentaje = f"{filtro_model_id.porcentaje}"
                    tiempo_total = round(sum(filtro_model_id.tiempos_id.mapped("tiempo")),2)
                result.append({
                    'primera_pieza':True,
                    'archivo':primera.nombre,
                    'material': f"{primera.material_ids.id} - {primera.material_ids.nombre} {primera.material_ids.medida}",
                    'cantidad':primera.cantidad,
                    'tiempo_teorico':primera.tiempo_teorico,
                    'cortadora':primera.maquina,
                    'porcentaje':porcentaje,
                    'tiempo_real':tiempo_total
                })
        if orden_id.cortadora_id:
            for segunda in orden_id.primera_pieza_id:
                en_corte_id = request.env['dtm.documentos.cortadora'].sudo().search([('nombre', '=', segunda.nombre)])
                filtro_model_id = en_corte_id.filtered(
                    lambda record: record.model_id.orden_trabajo == orden and record.model_id.revision_ot == revision)
                finalizado_id = request.env['dtm.documentos.finalizados'].sudo().search(
                    [('nombre', '=', segunda.nombre)])
                filtro_finalizado_id = finalizado_id.filtered(
                    lambda record: record.model_id.orden_trabajo == orden and record.model_id.revision_ot == revision)

                if filtro_finalizado_id:
                    porcentaje = '100%'
                    tiempo_total = round(sum(filtro_finalizado_id.tiempos_id.mapped("tiempo")),2)
                elif filtro_model_id:
                    porcentaje = f"{filtro_model_id.porcentaje}"
                    tiempo_total = round(sum(filtro_model_id.tiempos_id.mapped("tiempo")),2)
                result.append({
                    'primera_pieza': True,
                    'archivo': segunda.nombre,
                    'material': f"{segunda.material_ids.id} - {segunda.material_ids.nombre} {segunda.material_ids.medida}",
                    'cantidad': segunda.cantidad,
                    'tiempo_teorico': segunda.tiempo_teorico,
                    'cortadora': segunda.maquina,
                    'porcentaje': porcentaje,
                    'tiempo_real': tiempo_total
                })
        return result
      
    # Carga los maquinados y sus estados
    @http.route('/seguimiento_maquinados', type='json', auth='public')
    def lista_maquinados(self):
        raw = request.httprequest.data
        data = json.loads(raw)
        orden = data.get('orden')
        version = data.get('version')
        get_maquinados = request.env['dtm.maquinados'].sudo().search([('orden_trabajo','=',orden),('revision_ot','=',version)])
        get_finalizados = request.env['dtm.maquinados.terminados'].sudo().search([('orden_trabajo','=',orden),('revision_ot','=',version)])
        result = []
        if get_finalizados:
            for maquinado in get_finalizados.maquinados_id:
                result.append({
                    'nombre':maquinado.nombre,
                    'cantidad':maquinado.cantidad,
                    'porcentaje':'100%',
                    'tiempo':maquinado.tiempo_total,                    
                })
        elif get_maquinados:
            for maquinado in get_maquinados.maquinados_id:
                result.append({                    
                    'nombre':maquinado.nombre,
                    'cantidad':maquinado.cantidad,
                    'porcentaje':f"{round(maquinado.status,2)}%",
                    'tiempo':round(sum(maquinado.tiempos_id.mapped("tiempo")),2),                    
                })

        return result

    # Carga los datos de las máquinas de corte en uso
    @http.route('/maquinas_corte', type='http', auth='public')
    def maquinas_corte(self):
        get_play = request.env['dtm.documentos.cortadora'].sudo().search([('start','=',True)])
        result = []
        for maquina in get_play:
            result.append({
                'nombre':f"{maquina.model_id.orden_trabajo} - {maquina.model_id.nombre_orden}",                
                'primera_pieza':maquina.model_id.primera_pieza,
                'archivo':maquina.nombre,
                'cantidad':maquina.cantidad,
                'contador':maquina.contador,
                'lamina':maquina.lamina,
                'tiempo':round(maquina.tiempo_total,2),
                'porcentaje':round(maquina.porcentaje,2),
                'cortadora':maquina.cortadora,
            })
        return request.make_response(
            json.dumps(result),
            headers={
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin':'*'
            }
        )
