from odoo import http
from odoo.http import request,Response
import json
from datetime import datetime,date,timedelta
class ProcesosController(http.Controller):
    # Carga las ordenes de trabajo y su estado en los procesos
    @http.route('/seguimiento_procesos', type='http', auth='public')
    def ordenes_trabajo(self, **kwargs):
        # Se obtienen todas las ordenes de trabajo
        ordenes_trabajo = request.env['dtm.odt'].sudo().search([])
        result = []
        for orden in ordenes_trabajo:
            procesos_id = request.env['dtm.proceso'].sudo().search([('ot_number','=',orden.ot_number),('revision_ot','=',orden.revision_ot)],limit=1)
            retardo = True if orden.date_rel < date.today() else False
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
                    'fecha_retardo':retardo,
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
                    'status':dict(procesos_id._fields['status'].selection).get(procesos_id.status) if dict(procesos_id._fields['status'].selection).get(procesos_id.status) else ''
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
                filtro_model_id = en_corte_id.filtered(lambda record: record.model_id.orden_trabajo == orden and record.model_id.revision_ot == revision and record.model_id.primera_pieza==True)
                finalizado_id = request.env['dtm.documentos.finalizados'].sudo().search([('nombre','=',primera.nombre)])
                filtro_finalizado_id = finalizado_id.filtered(lambda  record:record.model_id.orden_trabajo == orden and record.model_id.revision_ot == revision and record.model_id.primera_pieza==True)
                # Si está en finalizado el porcentaje está en 100 y si no se pone el porcentaje real del corte
                if filtro_finalizado_id:
                    porcentaje = '100%'
                    tiempo_total = round(sum(filtro_finalizado_id.tiempos_id.mapped("tiempo")),2)
                elif filtro_model_id:
                    porcentaje = f"{round(filtro_model_id.porcentaje,2)}"
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
            for segunda in orden_id.cortadora_id:
                en_corte_id = request.env['dtm.documentos.cortadora'].sudo().search([('nombre', '=', segunda.nombre)])
                filtro_model_id = en_corte_id.filtered(
                    lambda record: record.model_id.orden_trabajo == orden and record.model_id.revision_ot == revision and record.model_id.primera_pieza == False)
                finalizado_id = request.env['dtm.documentos.finalizados'].sudo().search(
                    [('nombre', '=', segunda.nombre)])
                filtro_finalizado_id = finalizado_id.filtered(
                    lambda record: record.model_id.orden_trabajo == orden and record.model_id.revision_ot == revision and record.model_id.primera_pieza == False)
                if filtro_finalizado_id:
                    porcentaje = '100%'
                    tiempo_total = round(sum(filtro_finalizado_id.tiempos_id.mapped("tiempo")),2)
                elif filtro_model_id:
                    porcentaje = f"{round(filtro_model_id.porcentaje,2)}"
                    tiempo_total = round(sum(filtro_model_id.tiempos_id.mapped("tiempo")),2)
                result.append({
                    'primera_pieza': False,
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
                'cliente':request.env['dtm.odt'].sudo().search([('ot_number','=',maquina.model_id.orden_trabajo),('revision_ot','=',maquina.model_id.revision_ot)],limit=1).name_client,
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

    # Busca todos los archivos pendientes a cortar
    @http.route('/corte_diario', type='http', auth='public')
    def corte_diario(selfs):

        get_cortes = request.env['dtm.documentos.cortadora'].sudo().search([('fecha_corte','!=',False)])
        cortes = get_cortes.filtered(
            lambda r: r.fecha_corte and (r.fecha_corte <= date.today())
        )
        cortes_validos = cortes.filtered(
            lambda r: round(r.porcentaje < 100,2) and (r.fecha_corte < date.today())
        )
        # print(cortes_validos)
        result = [{
                    'nombre':f"{maquina.model_id.orden_trabajo} - {maquina.model_id.nombre_orden}",
                    'cliente':request.env['dtm.odt'].sudo().search([('ot_number','=',maquina.model_id.orden_trabajo),('revision_ot','=',maquina.model_id.revision_ot)],limit=1).name_client,
                    'primera_pieza': maquina.model_id.primera_pieza,
                    'archivo': maquina.nombre,
                    'cantidad': maquina.cantidad,
                    'contador': maquina.contador,
                    'lamina': maquina.lamina,
                    'tiempo_teorico': round(maquina.tiempo_teorico, 2) if maquina.tiempo_teorico else 0,
                    'porcentaje': round(maquina.porcentaje, 2),
                    'cortadora': maquina.cortadora,
                    'prioridad':maquina.priority,
                    'play':maquina.start,
                    'tiempo_real':round(maquina.tiempo_total, 2) if maquina.tiempo_total else 0,
                    'fecha_corte':maquina.fecha_corte.strftime('%x')
                } for maquina in cortes_validos]
        # Se sortea por prioridad
        result = sorted(result, key=lambda x: (datetime.strptime(x['fecha_corte'],'%d/%m/%Y'),-1*int(x['prioridad'])))
        return request.make_response(
            json.dumps(result),
            headers={
                'Content-Type':'application/json',
                'Access-Control-Allow-Origin':'*'
            }
        )

    # Obtiene los tiempos del día en curso
    @http.route('/corte_tiempos',type='http',auth='public')
    def corte_tiempos(self):
        hoy = date.today()
        inicio = datetime.combine(hoy, datetime.min.time())  # 00:00:00
        fin = datetime.combine(hoy + timedelta(days=1), datetime.min.time())  # mañana 00:00:00

        get_cortes = request.env['dtm.documentos.tiempos'].search([
            ('create_date', '>=', inicio),
            ('create_date', '<', fin)
        ])
        maquina_mit = 0
        maquina_jfy = 0
        for nesteo in get_cortes:
            if nesteo.model_id.cortadora == 'MITSUBISHI':
                maquina_mit += nesteo.tiempo

            if nesteo.model_id.cortadora == 'BFC6025':
                maquina_jfy += nesteo.tiempo


        result = {
                    'mitsubishi':round(maquina_mit,2),
                    'jfy':round(maquina_jfy,2)
                  }

        return request.make_response(
            json.dumps(result),
            headers={
                'Content-Type':'application/json',
                'Access-Control-Allow-Origin':'*'
            }
        )

    # Obtienes la lista de materiales que faltan por liberar según la orden de trabajo que lo solicite
    @http.route('/liberar_materiales', type='json', auth='public')
    def liberar_materiales(self):
        raw = request.httprequest.data
        data = json.loads(raw)
        orden = data.get('orden')
        revision = data.get('version')

        orden_id = request.env['dtm.compras.requerido'].sudo().search([('orden_trabajo','=',orden),('revision_ot','=',revision),('tipo_orden','in',['OT','NPI'])])

        result = [{
                'codigo': material.codigo,
                'descripcion': material.nombre,
                'cantidad': material.cantidad,
                'proveedor': request.env['dtm.compras.material'].sudo().search([('nombre','=',material.nombre)],limit=1).proveedor_id.nombre,
                'unitario':request.env['dtm.compras.material'].sudo().search([('nombre','=',material.nombre)],limit=1).unitario,
                'total': round(request.env['dtm.compras.material'].sudo().search([('nombre','=',material.nombre)],limit=1).unitario * material.cantidad,2),
                'nesteo': 'Falta' if material.nesteo else 'Si',
            } for material in orden_id]
        return result
    
    # Obtienes la lista de materiales que faltan de comprar según la orden de trabajo que lo solicite
    @http.route('/compra_material', type='json', auth='public')
    def compra_material(self):
        raw = request.httprequest.data
        data = json.loads(raw)
        orden = data.get('orden')
        revision = data.get('version')

        orden_id = request.env['dtm.compras.realizado'].sudo().search([('orden_trabajo','=',orden),('revision_ot','=',revision),('tipo_orden','in',['OT','NPI']),('listo_btn','!=',True)])

        result = [{
                'codigo': material.codigo,
                'descripcion': material.nombre,
                'cantidad': material.cantidad,
                'proveedor': material.proveedor,
                'unitario':material.unitario,
                'total': round(material.unitario * material.cantidad,2),
            } for material in orden_id]
        return result
