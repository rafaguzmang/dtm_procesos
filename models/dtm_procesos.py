from odoo import api,models,fields
import re
from datetime import datetime

class Proceso(models.Model):
    _name = "dtm.proceso"
    _inherit = ['mail.thread']
    _description = "Modulo para indicar el status de la ODT o NPI"
    _order = "ot_number desc"

    status = fields.Selection(string="Estatus", selection=[("aprobacion","Pendiente a aprobación"),
                                         ("corte","Corte"),("corterevision","Corte - Revisión FAI"),
                                         ("revision","Revisión FAI"),("corterevision","Corte - Revisión FAI"),
                                         ("cortedoblado","Corte - Doblado"),("doblado","Doblado"),
                                         ("soldadura","Soldadura"),("lavado","Lavado"),("pintura","Pintura"),
                                         ("ensamble","Ensamble"),("calidad","Calidad"),("instalacion","Instalación"),
                                         ("terminado","Terminado")])

    sequence = fields.Integer()
    ot_number = fields.Char(string="NÚMERO",readonly=True)
    tipe_order = fields.Char(string="TIPO",readonly=True)
    name_client = fields.Char(string="CLIENTE",readonly=True)
    product_name = fields.Char(string="NOMBRE",readonly=True)
    date_in = fields.Date(string="FECHA DE ENTRADA", readonly=True)
    po_number = fields.Char(string="PO",readonly=True)
    date_rel = fields.Date(string="FECHA DE ENTREGA",readonly=True)
    version_ot = fields.Integer(string="VERSIÓN OT",readonly=True)
    color = fields.Char(string="COLOR",readonly=True)
    cuantity = fields.Integer(string="CANTIDAD",readonly=True)
    materials_ids = fields.Many2many("dtm.materials.line",readonly=True)
    materials_npi_ids = fields.Many2many("dtm.materials.npi",readonly=True)
    planos = fields.Boolean(string="Planos",default=False,readonly=True)
    nesteos = fields.Boolean(string="Nesteos",default=False,readonly=True)

    rechazo_id = fields.Many2many("dtm.odt.rechazo",readonly=False)
    rechazo_npi_id = fields.Many2many("dtm.npi.rechazo",readonly=False)

    anexos_id = fields.Many2many("dtm.proceso.anexos",readonly=True)
    cortadora_id = fields.Many2many("dtm.proceso.cortadora",readonly=True)
    primera_pieza_id = fields.Many2many("dtm.proceso.primer",readonly=True)
    tubos_id = fields.Many2many("dtm.proceso.tubos",readonly=True)


    material_cortado = fields.Boolean(default=False)

    firma = fields.Char(string="Firma", readonly = True)
    firma_compras = fields.Char(string = "Compras", readonly = True)
    firma_diseno = fields.Char(string = "Diseñador", readonly = True)
    firma_parcial = fields.Boolean()
    firma_almacen = fields.Char(string = "", readonly = True)
    firma_ventas = fields.Char(string = "Ventas", readonly = True)
    firma_calidad = fields.Char(string = "", readonly = True)
   
    firma_compras_kanba = fields.Char(string = "Compras", readonly = True)
    firma_diseno_kanba = fields.Char(string = "Diseñador", readonly = True)
    firma_almacen_kanba = fields.Char(string = "", readonly = True)
    firma_ventas_kanba = fields.Char(string = "Ventas", readonly = True)
    firma_calidad_kanba = fields.Char(string = "", readonly = True)

    #---------------------Resumen de descripción------------
    description = fields.Text(string= "DESCRIPCIÓN",placeholder="RESUMEN DE DESCRIPCIÓN")

    notes = fields.Text()

    #---------------------Evento para detener el proceso------------------------------------

    pausado = fields.Char(string="Detenido por: ", readonly=True)
    status_pausado = fields.Char()
    pausa_motivo = fields.Text()

    materials = fields.Integer(string="Material", compute="_compute_materials")

    @api.onchange("status")
    def _action_status(self):
        if not self.firma_compras_kanba or not self.firma_almacen_kanba or not self.firma_ventas_kanba or not self.firma:
            self.status = "aprobacion"

    @api.depends("materials_ids")
    def _compute_materials(self):
        for record in self:
            total = len(record.materials_ids)
            cont = 0
            if record.materials_ids:
                for material in record.materials_ids:
                    if material.materials_required == 0:
                        cont += 1
                record.materials = cont * 100 / total
            else:
                record.materials = 0


    def get_view(self, view_id=None, view_type='form', **options):
        res = super(Proceso,self).get_view(view_id, view_type,**options)
        get_self = self.env['dtm.proceso'].search([])
        for get in get_self:
            if get.status != "terminado" or get.status != "calidad" or get.status != "instalacion":
                if not get.firma_compras_kanba or not get.firma_almacen_kanba or not get.firma_ventas_kanba or not get.firma:
                        get.status = "aprobacion"

            if get.status == "terminado" and not get.firma_calidad_kanba:
                get.status = "calidad"

            if get.firma_calidad_kanba and get.status != "instalacion":
                get.status = "terminado"

        get_facturas = self.env['dtm.ordenes.compra.facturado'].search([])
        for factura in get_facturas:
            for orden in factura.descripcion_id:
                get_proceso = self.env['dtm.proceso'].search([("ot_number","=",orden.orden_trabajo)])
                if get_proceso:
                    get_diseno = self.env['dtm.odt'].search([("ot_number","=",get_proceso.ot_number)])
                    get_almacen = self.env['dtm.almacen.odt'].search([("ot_number","=",get_proceso.ot_number)])
                    get_calidad = self.env['dtm.calidad'].search([("ot_number","=",get_proceso.ot_number)])
                    get_ventas = self.env['dtm.ventas.ot'].search([("ot_number","=",get_proceso.ot_number)])
                    get_compras = self.env['dtm.compras.odt'].search([("ot_number","=",get_proceso.ot_number)])
                    vals = {
                        "status": factura.factura,
                        "ot_number": get_proceso.ot_number,
                        "tipe_order": get_proceso.tipe_order,
                        "name_client": get_proceso.name_client,
                        "product_name": get_proceso.product_name,
                        "date_in": get_proceso.date_in,
                        "po_number": get_proceso.po_number,
                        "date_rel": get_proceso.date_rel,
                        "version_ot": get_proceso.version_ot,
                        "color": get_proceso.color,
                        "cuantity": get_proceso.cuantity,
                        "materials_ids": get_proceso.materials_ids,
                        "planos": get_proceso.planos,
                        "nesteos": get_proceso.nesteos,
                        "rechazo_id":get_proceso.rechazo_id,
                        "anexos_id":get_proceso.anexos_id,
                        "cortadora_id":get_proceso.cortadora_id,
                        "primera_pieza_id":get_proceso.primera_pieza_id,
                        "tubos_id":get_proceso.tubos_id,
                        "firma": get_proceso.firma,
                        "firma_compras": get_proceso.firma_compras,
                        "firma_diseno": get_proceso.firma_diseno,
                        "firma_almacen": get_proceso.firma_almacen,
                        "firma_ventas": get_proceso.firma_ventas,
                        "description": get_proceso.description,
                        "firma_calidad":get_proceso.firma_calidad
                    }
                    get_facturado = self.env['dtm.facturado.odt'].search([("ot_number","=",get_proceso.ot_number)])
                    if not get_facturado:
                        get_facturado.create(vals)
                    else:
                        get_facturado.write(vals)
                    get_diseno.unlink()
                    get_almacen.unlink()
                    get_calidad.unlink()
                    get_ventas.unlink()
                    get_compras.unlink()
                    get_proceso.unlink()
        return res

    def action_liberar(self):
        vals = {
            "orden_trabajo":self.ot_number,
            "fecha_entrada": datetime.today(),
            "nombre_orden":self.product_name,
            "tipo_orden": "OT"
        }
        get_corte = self.env['dtm.materiales.laser'].search([("orden_trabajo","=",self.ot_number)])
        get_corte_realizado = self.env['dtm.laser.realizados'].search([("orden_trabajo","=",self.ot_number)])
        if get_corte_realizado:
            get_corte_realizado.unlink() #Quita la orden del apartado realizado para poder incluir los siguientes archivos
        if get_corte:
            get_corte.write(vals)
        else:
            get_corte.create(vals)
            get_corte = self.env['dtm.materiales.laser'].search([("orden_trabajo","=",self.ot_number)])
        get_corte.write({'cortadora_id': [(5, 0, {})]})
        lines = []
        for anexo in self.cortadora_id:
            vals = {
                "documentos":anexo.documentos,
                "nombre":anexo.nombre,
                "primera_pieza": False
            }
            get_anexos = self.env['dtm.documentos.cortadora'].search([("nombre","=",anexo.nombre)])
            if get_anexos:
                get_anexos.write(vals)
                lines.append(get_anexos.id)
            else:
                get_anexos.create(vals)
                get_anexos = self.env['dtm.documentos.cortadora'].search([("nombre","=",anexo.nombre)])
                lines.append(get_anexos.id)
        get_corte.write({'cortadora_id': [(6, 0, lines)]})
        lines = []
        get_corte.write({'materiales_id': [(5, 0, {})]})
        for lamina in self.materials_ids:
            if re.match("Lámina",lamina.nombre):
                get_almacen = self.env['dtm.materiales'].search([("codigo","=",lamina.materials_list.id)])
                content = {
                    "identificador": lamina.materials_list.id,
                    "nombre": lamina.nombre,
                    "medida": lamina.medida,
                    "cantidad": lamina.materials_cuantity,
                    "inventario": lamina.materials_inventory,
                    "requerido": lamina.materials_required,
                    "localizacion": get_almacen.localizacion
                }

                get_cortadora_laminas = self.env['dtm.cortadora.laminas'].search([
                    ("identificador","=",lamina.materials_list.id),("nombre","=",lamina.nombre),
                    ("medida","=",lamina.medida),("cantidad","=",lamina.materials_cuantity),
                    ("inventario","=",lamina.materials_inventory),("requerido","=",lamina.materials_required),
                    ("localizacion","=",get_almacen.localizacion)])

                if get_cortadora_laminas:
                    get_cortadora_laminas.write(content)
                    lines.append(get_cortadora_laminas.id)
                else:
                    get_cortadora_laminas.create(content)
                    get_cortadora_laminas = self.env['dtm.cortadora.laminas'].search([
                    ("identificador","=",lamina.materials_list.id),("nombre","=",lamina.nombre),
                    ("medida","=",lamina.medida),("cantidad","=",lamina.materials_cuantity),
                    ("inventario","=",lamina.materials_inventory),("requerido","=",lamina.materials_required),
                    ("localizacion","=",get_almacen.localizacion)])
                    lines.append(get_cortadora_laminas.id)
        get_corte.write({"materiales_id":[(6, 0,lines)]})

    def action_firma(self):
        self.firma = self.env.user.partner_id.name
        get_ot = self.env['dtm.odt'].search([("ot_number","=",self.ot_number)])
        get_ot.write({"firma_produccion": self.firma})
        # get_corte = self.env['dtm.materiales.las.

        # if self.rechazo_id:
        #     for rechazo in self.rechazo_id:
        #         print(rechazo.model_id)

    def action_imprimir_formato(self): # Imprime según el formato que se esté llenando
        return self.env.ref("dtm_procesos.formato_orden_de_trabajo").report_action(self)

    def action_imprimir_materiales(self): # Imprime según el formato que se esté llenando
        return self.env.ref("dtm_procesos.formato_lista_materiales").report_action(self)

class TestModelLine(models.Model):
    _name = "dtm.proceso.materials"
    _description = "Tabla de materiales"

    nombre = fields.Char(string="MATERIAL")
    medida = fields.Char(string="MEDIDA")
    materials_cuantity = fields.Integer(string="CANTIDAD")
    materials_inventory = fields.Integer(string="INVENTARIO")
    materials_required = fields.Integer(string="REQUERIDO")

class Rechazo(models.Model):
    _name = "dtm.proceso.rechazo"
    _description = "Tabla para llenar los motivos por el cual se rechazo la ODT"

    descripcion = fields.Text(string="Descripción del Rechazo")
    fecha = fields.Date(string="Fecha")
    hora = fields.Char(string="Hora")
    firma = fields.Char(string="Firma")

class Documentos(models.Model):
    _name = "dtm.proceso.anexos"
    _description = "Guarda todos los planos de la orden de trabajo"

    documentos = fields.Binary()
    nombre = fields.Char()
    color = fields.Integer(string='Color', readonly = False)

    def action_mas(self):
        self.color += 1

    def action_menos(self):
        self.color -= 1
        if self.color < 0:
            self.color = 0

class Cortadora(models.Model):
    _name = "dtm.proceso.cortadora"
    _description = "Guarda los nesteos del Radán"

    documentos = fields.Binary()
    nombre = fields.Char()
    cortado = fields.Char("Cortado")

class CortadoraPrimera(models.Model):
    _name = "dtm.proceso.primer"
    _description = "Guarda los nesteos del Radán para primer corte"

    documentos = fields.Binary()
    nombre = fields.Char()
    cortado = fields.Char("Cortado")

class Tubos(models.Model):
    _name = "dtm.proceso.tubos"
    _description = "Guarda los nesteos de la cortadora de tubos"

    documentos = fields.Binary()
    nombre = fields.Char()
    cortado = fields.Char("Cortado")

