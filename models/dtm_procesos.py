from odoo import api,models,fields,http
import re
from datetime import datetime
from odoo.exceptions import ValidationError, AccessError, MissingError,Warning
import json
class Proceso(models.Model):
    _name = "dtm.proceso"
    _inherit = ['mail.thread']
    _description = "Modulo para indicar el status de la ODT o NPI"
    _order = "ot_number desc"
    _rec_name = "ot_number"



    status = fields.Selection(string="Estatus", selection=[("aprobacion","Nesteo"),
                                         ("corte","Corte"),("revision","Revisión FAI"),("doblado","Doblado"),
                                         ("soldadura","Soldadura"),("maquinado","Maquinado"),("pintura","Pintura"),
                                         ("ensamble","Ensamble"),("externo","Servicio Externo"),("calidad","Calidad"),("instalacion","Instalación"),
                                         ("terminado","Terminado")])

    sequence = fields.Integer()
    ot_number = fields.Char(string="NÚMERO",readonly=True)
    tipe_order = fields.Char(string="TIPO",readonly=True)
    name_client = fields.Char(string="CLIENTE",readonly=True)
    product_name = fields.Char(string="NOMBRE",readonly=True)
    date_in = fields.Date(string="ENTRADA", readonly=True)
    po_number = fields.Char(string="PO",readonly=True)
    date_rel = fields.Date(string="ENTREGA",readonly=True)
    version_ot = fields.Integer(string="VERSIÓN OT",readonly=True)
    color = fields.Char(string="COLOR",readonly=True)
    cuantity = fields.Integer(string="CANTIDAD",readonly=True)
    materials_ids = fields.Many2many("dtm.materials.line",readonly=True)
    # materials_npi_ids = fields.Many2many("dtm.materials.npi",readonly=True)
    planos = fields.Boolean(string="Planos",default=False,readonly=True)
    nesteos = fields.Boolean(string="Nesteos",default=False,readonly=True)
    date_terminado = fields.Date(string="Finalización",readonly=True)

    rechazo_id = fields.One2many("dtm.proceso.rechazo",'model_id',readonly=False)
    rechazo_npi_id = fields.Many2many("dtm.npi.rechazo",readonly=False)

    anexos_id = fields.Many2many("dtm.proceso.anexos",readonly=True)
    cortadora_id = fields.Many2many("dtm.proceso.cortadora",readonly=True)
    primera_pieza_id = fields.Many2many("dtm.proceso.primer",readonly=True)
    tubos_id = fields.Many2many("dtm.proceso.tubos",readonly=True)

    material_cortado = fields.Boolean(default=False)

    firma = fields.Char(string="Firma", readonly = True)
    firma_compras = fields.Char(readonly = True)
    firma_diseno = fields.Char(string = "Diseñador", readonly = True)
    firma_parcial = fields.Boolean()
    firma_almacen = fields.Char(readonly = True)
    firma_ventas = fields.Char(readonly = True)
    firma_calidad = fields.Char(readonly = True)
   
    firma_compras_kanba = fields.Char( readonly = True)
    firma_diseno_kanba = fields.Char(readonly = True)
    firma_almacen_kanba = fields.Char(readonly = True)
    firma_ventas_kanba = fields.Char(readonly = True)
    firma_calidad_kanba = fields.Char(readonly = True)

    #---------------------Resumen de descripción------------
    description = fields.Text(string= "DESCRIPCIÓN")

    notes = fields.Text()

    #---------------------Evento para detener el proceso------------------------------------

    pausado = fields.Char(string="Detenido por: ", readonly=True)
    pausa = fields.Boolean()
    status_pausado = fields.Char()

    user_pausa = fields.Boolean(compute="_compute_user_email_match")

    materials = fields.Integer(string="Material")

    #Calidad - Libarción de primera pieza
    calidad_liberacion = fields.One2many("dtm.proceso.liberacion","model_id")

    #Campo para guardar archivos de certificación
    anexos_certificacion = fields.Many2many("ir.attachment",string="Archivos")

    def action_pasive(self):
        pass

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False, url_ordenes=None):
        # Obtener el parámetro 'ordenes' del contexto
        params = self.env.context.get('params', {})
        ordenes = params.get('ordenes', '')
        if ordenes:
            list_ordenes = str(ordenes).split(" ")
            args += [('ot_number', 'in',list_ordenes)]
        records = super(Proceso, self).search(args, offset=offset, limit=limit, order=order, count=count)
        return records

    def action_devolver(self):
        if self.notes:
            get_odt = self.env['dtm.odt'].search([("ot_number","=",self.ot_number),("tipe_order","=",self.tipe_order)])
            day = int(get_odt.date_disign_finish.strftime('%j'))+1 if get_odt.date_disign_finish else datetime.now().strftime('%j') + 1
            year = int(get_odt.date_disign_finish.strftime('%Y')) if get_odt.date_disign_finish else datetime.now().strftime('%Y')
            fecha = datetime.strptime(f"{year}-{day}", "%Y-%j").date()
            get_odt.write({
                'version_ot':get_odt.version_ot+1,
                'notes':f"{get_odt.notes}\n\n Motivo de rechazo ({get_odt.version_ot+1}):\n {self.notes} \n Rechaza: {self.env.user.partner_id.name}" if get_odt.notes else f"Motivo de rechazo ({get_odt.version_ot+1}):\n {self.notes} \n Rechaza: {self.env.user.partner_id.name}" ,
                'date_disign_finish':fecha
            })
            self.unlink()
        else:
            raise ValidationError('Favor de especificar en la pestaña de "NOTAS" motivo del rechazo')



    def action_detener(self):
        email = self.env.user.partner_id.email
        if email == 'calidad@dtmindustry.com' or email == 'calidad2@dtmindustry.com':
            self.pausado= "Pausado por Calidad"
        elif email == 'hugo_chacon@dtmindustry.com'or email=='ventas1@dtmindustry.com' or email=="rafaguzmang@hotmail.com":
            self.pausado= "Pausado por Ventas"
        self.status_pausado= self.status
        self.pausa = True

    def action_continuar(self):
        self.pausado = ""
        self.status_pausado = ""
        self.pausa = False
    #Obtiene el email del usuario
    def _compute_user_email_match(self):
        for record in self:
            email = self.env.user.partner_id.email
            emails = ['calidad@dtmindustry.com','calidad2@dtmindustry.com','hugo_chacon@dtmindustry.com',
                      'ventas1@dtmindustry.com','rafaguzmang@hotmail.com','manufactura@dtmindustry.com','ingenieria1@dtmindustry.com']
            record.user_pausa = False
            if email in emails:
                record.user_pausa = True

    def get_view(self, view_id=None, view_type='form', **options):
        res = super(Proceso,self).get_view(view_id, view_type,**options)
        get_self = self.env['dtm.proceso'].search([]) #No permite el cambio a terminado sin firma de calidad
        for get in get_self:
            if get.status == "terminado" and not get.firma_calidad_kanba:
                get.status = "calidad"

            if get.firma_calidad_kanba and get.status != "instalacion":
                get.status = "terminado"

        get_materiales = self.env['dtm.proceso'].search([])
        for record in get_materiales: # Actualiza la lista de materiales de las ordenes
            # if record.tipe_order == "OT":
            materiales = record.materials_ids
            # else:
            #     materiales = record.materials_npi_ids
            total = len(materiales)
            cont = 0
            if materiales:
                for material in materiales:
                    if material.materials_required == 0:
                        cont += 1
                record.materials = cont * 100 / total
            else:
                record.materials = 0
        return res

    def eliminacion_ot (self,get_ordenes):
        for po in get_ordenes:
            ordenes = self.env['dtm.proceso'].search([("po_number","=",po),("status","=","terminado")]).mapped('ot_number')
            for orden in ordenes:
                get_proceso = self.env['dtm.proceso'].search([("ot_number","=",int(orden)),("tipe_order","=","OT")])
                vals = {
                        "status": self.env['dtm.ordenes.compra.facturado'].search([("orden_compra","=",get_proceso.po_number)], limit=1).factura,
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
                        # "materials_ids": get_proceso.materials_ids,
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
                        "firma_calidad":get_proceso.firma_calidad,
                        "calidad_liberacion":get_proceso.calidad_liberacion,
                        "date_terminado":self.date_terminado,
                    }
                get_facturado = self.env['dtm.facturado.odt'].search([("ot_number","=",get_proceso.ot_number)])
                get_facturado.write(vals) if get_facturado else get_facturado.create(vals)
                get_facturado = self.env['dtm.facturado.odt'].search([("ot_number","=",get_proceso.ot_number)])
                get_facturado.write({'materieales_id': [(5, 0, {})]})
                lines = []
                for item in get_proceso.materials_ids:#Se agrega o se actualiza material de la tabla dtm.facturado.materiales y se obtienen los id para casarlos con la orden correspondiente
                    valmat = {
                        "material":f"{item.nombre} {item.medida}",
                        "cantidad":item.materials_cuantity,
                    }
                    get_facturado_material = self.env['dtm.facturado.materiales'].search([("material","=",f"{item.nombre} {item.medida}"),("cantidad","=",item.materials_cuantity)])
                    get_facturado_material.write(valmat) if get_facturado_material else get_facturado_material.create(valmat)
                    get_facturado_material = self.env['dtm.facturado.materiales'].search([("material","=",f"{item.nombre} {item.medida}"),("cantidad","=",item.materials_cuantity)])
                    lines.append(get_facturado_material.id)
                get_facturado.write({'materieales_id': [(6, 0, lines)]})
                #-------------------------------------------------------------------------------------------------------------------------------
                if get_facturado:
                    self.env['dtm.odt'].search([('ot_number','=',int(orden))]).unlink()
                    self.env['dtm.compras.odt'].search([('ot_number','=',int(orden))]).unlink()
                    self.env['dtm.proceso'].search([('ot_number','=',int(orden))]).unlink()
                    self.env['dtm.compras.realizado'].search([('orden_trabajo','=',int(orden))]).unlink()

    def action_liberar(self):
        email = self.env.user.partner_id.email
        get_realizados = self.env['dtm.laser.realizados'].search([("orden_trabajo","=",self.ot_number),("tipo_orden","=",self.tipe_order),("primera_pieza","=",True)])
        if email in ['calidad@dtmindustry.com', 'calidad2@dtmindustry.com','rafaguzmang@hotmail.com'] and get_realizados:
            vals = {
                "orden_trabajo":self.ot_number,
                "fecha_entrada": datetime.today(),
                "nombre_orden":self.product_name,
                "tipo_orden": "OT",
                "primera_pieza": False
            }
            get_corte = self.env['dtm.materiales.laser'].search([("orden_trabajo","=",self.ot_number)])
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
                get_anexos = self.env['dtm.documentos.cortadora'].search([("nombre","=",anexo.nombre)],limit=1)
                if get_anexos:
                    vals['cortado']= False
                    vals['estado']=""
                    get_anexos.write(vals)
                    lines.append(get_anexos.id)
                else:
                    get_anexos.create(vals)
                    get_anexos = self.env['dtm.documentos.cortadora'].search([("nombre","=",anexo.nombre)],limit=1)
                    lines.append(get_anexos.id)
            get_corte.write({'cortadora_id': [(6, 0, lines)]})
            lines = []
            get_corte.write({'materiales_id': [(5, 0, {})]})
            for lamina in self.materials_ids:
                if re.match("Lámina",lamina.nombre):
                    get_almacen = self.env['dtm.materiales'].search([("codigo","=",lamina.materials_list.id)],limit=1)
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
        else:
            raise ValidationError("Esta orden sigue en corte de Primera pieza")

    # Función para registrar los rechasos en el modulo de calidad
    def action_rechazo(self):
        get_calidad = self.env['dtm.calidad.rechazo'].search([('job_no','=',self.ot_number)]).mapped('consecutivo')

        for exist in self.rechazo_id:
            if exist.serial_no in get_calidad:
                self.env['dtm.calidad.rechazo'].search([('consecutivo','=',exist.serial_no)]).write({
                    'po_number':self.po_number,
                    'part_no':self.product_name,
                    'no_of_pieces_rejected':exist.no_of_pieces_rejected,
                    'reason':exist.reason,
                    'inspector':exist.inspector,
                    'date':exist.date,
                })
            else:
                # self.env.cr.execute(f"SELECT setval('dtm_calidad_rechazo_id_seq', {exist.serial_no}, false);")
                self.env['dtm.calidad.rechazo'].create({
                    'consecutivo':exist.serial_no,
                    'job_no':self.ot_number,
                    'po_number':self.po_number,
                    'part_no':self.product_name,
                    'no_of_pieces_rejected':exist.no_of_pieces_rejected,
                    'reason':exist.reason,
                    'inspector':exist.inspector,
                    'date':exist.date,
                })


    def action_firma(self):
        email = self.env.user.partner_id.email
        if email == 'manufactura@dtmindustry.com':
            self.firma = self.env.user.partner_id.name
            if self.status == 'calidad':
                self.date_terminado = datetime.now();
        if email in ['calidad@dtmindustry.com','calidad2@dtmindustry.com',"rafaguzmang@hotmail.com"]:
            if self.status == 'calidad' and not self.pausa:
                # Si es una OT la manda a terminado
                if self.tipe_order == 'OT':
                    self.firma_calidad =  self.env.user.partner_id.name,
                    self.firma_calidad_kanba = "Calidad"
                    self.status = 'terminado'
                elif self.tipe_order == 'NPI': #Si es un NPI lo manda a facturado
                    get_fact = self.env['dtm.facturado.npi'].search([('ot_number','=',self.ot_number),('tipe_order','=',self.tipe_order)])
                    vals = {
                        "status":self.status,
                        "ot_number":self.ot_number,
                        "tipe_order":self.tipe_order,
                        "name_client":self.name_client,
                        "product_name":self.product_name,
                        "date_in":self.date_in,
                        "po_number":self.po_number,
                        "date_rel":self.date_rel,
                        "version_ot":self.version_ot,
                        "color":self.color,
                        "cuantity":self.cuantity,
                        "firma":self.firma,
                        "firma_compras":self.firma_compras,
                        "firma_diseno":self.firma_diseno,
                        "firma_almacen":self.firma_almacen,
                        "firma_ventas":self.firma_ventas,
                        "firma_calidad":self.firma_calidad,
                        "description":self.description,
                        "rechazo_id":self.rechazo_id,
                        "anexos_id":self.anexos_id,
                        "calidad_liberacion":self.calidad_liberacion,
                        "date_terminado":self.date_terminado,
                    }
                    get_fact.write(vals) if get_fact else get_fact.create(vals)
                    get_fact = self.env['dtm.facturado.npi'].search([('ot_number','=',self.ot_number)])
                    lista = []
                    get_fact.write({'materieales_id': [(5, 0, {})]})
                    for material in self.materials_ids:
                        # print(material.nombre,material.medida)
                        vals = {
                            "npi_id":get_fact.id,
                            "material":f"{material.id} - {material.nombre} {material.medida}",
                            "cantidad":material.materials_cuantity
                        }
                        get_material = self.env['dtm.facturado.materiales'].search([("npi_id","=",get_fact.id),("material","=",f"{material.id} - {material.nombre} {material.medida}")])
                        get_material.write(vals) if get_material else get_material.create(vals)
                        get_material = self.env['dtm.facturado.materiales'].search([("npi_id","=",get_fact.id),("material","=",f"{material.id} - {material.nombre} {material.medida}")])
                        lista.append(get_material.id)
                    if get_fact:
                        get_fact.write({'materieales_id': [(6, 0, lista)]})
                        get_diseno = self.env['dtm.odt'].search([('ot_number','=',self.ot_number),('tipe_order','=',self.tipe_order)])
                        get_diseno.materials_ids.unlink()
                        get_diseno.unlink()
                        get_compras = self.env['dtm.compras.realizado'].search([('orden_trabajo','like',self.ot_number)])
                        get_compras.unlink()
                        get_self = self.env['dtm.proceso'].search([('ot_number','=',self.ot_number)])
                        get_self.unlink()
            else:
                raise ValidationError("OT/NPI debe de estar en status Calidad o faltan firmas")

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

    def serial_number(self):
        get_calidad = self.env['dtm.proceso.rechazo'].search([],order='serial_no desc', limit=1)
        return get_calidad.serial_no + 1 if get_calidad else 1

    model_id = fields.Many2one('dtm.proceso')
    serial_no = fields.Integer(string='SERIAL NO',default=serial_number,readonly=True)
    no_of_pieces_rejected = fields.Integer(string='NO. OF PIECES REJECTED')
    reason = fields.Text(string='REASON')
    inspector = fields.Selection(string='INSPECTOR',selection=[('leonardo','Leonardo Ramírez Ruiz')],default='leonardo')
    date = fields.Date(string='DATE',default=datetime.now(),readonly=True)
    revicion = fields.Selection(string='Revición',selection=[('muestreo','Muestreo'),('cien','100%')],default='cien')



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

class LiberacionPrimera(models.Model):
    _name = "dtm.proceso.liberacion"
    _description = "Liberación de primera pieza/única"

    model_id = fields.Many2one("dtm.proceso")
    fecha_revision = fields.Date(default= datetime.today(),readonly=True)

    #Funcional
    sujecion = fields.Selection(string="Sujeción correcta de la pieza.",selection=[("si","SI"),
                                         ("no","NO"),("na","NA")],default="na")
    puertas = fields.Selection(string="Las puertas abren y cierran con facilidad.",selection=[("si","SI"),
                                         ("no","NO"),("na","NA")],default="na")
    puertas_siguen = fields.Selection(string="Las puertas siguen cerradas con el moviento.",selection=[("si","SI"),
                                         ("no","NO"),("na","NA")],default="na")
    llantas = fields.Selection(string="Las llantas se mueven con facilidad.",selection=[("si","SI"),
                                         ("no","NO"),("na","NA")],default="na")
    rodillos = fields.Selection(string="Los rodillos se mueven con facilidad en el riel",selection=[("si","SI"),
                                         ("no","NO"),("na","NA")],default="na")
    #Estético
    acabado_pintura = fields.Selection(string="Acabado liso en pintura.",selection=[("si","SI"),
                                         ("no","NO"),("na","NA")],default="na")
    rayones = fields.Selection(string="Tiene rayones.",selection=[("si","SI"),
                                         ("no","NO"),("na","NA")],default="na")
    abolladuras = fields.Selection(string="Tiene aboyaduras.",selection=[("si","SI"),
                                         ("no","NO"),("na","NA")],default="na")
    saldadura = fields.Selection(string="Acabado limpio de soldadura.",selection=[("si","SI"),
                                         ("no","NO"),("na","NA")],default="na")
    pieza_limpia = fields.Selection(string="Pieza limpia.",selection=[("si","SI"),
                                         ("no","NO"),("na","NA")],default="na")
    #Mecánico
    todas_piezas = fields.Selection(string="Contiene todas las piezas indicadas en el plano.",selection=[("si","SI"),
                                         ("no","NO"),("na","NA")],default="na")
    ensamble_indicado = fields.Selection(string="Cuenta con el ensamble indicado en el plano.",selection=[("si","SI"),
                                         ("no","NO"),("na","NA")],default="na")
    saldadura_uniones = fields.Selection(string="Soldadura en todas las uniones de la pieza.",selection=[("si","SI"),
                                         ("no","NO"),("na","NA")],default="na")
    tornilleria = fields.Selection(string="Tornillería y remache de acuerdo al plano.",selection=[("si","SI"),
                                         ("no","NO"),("na","NA")],default="na")

    #Dimensiones
    dimensiones = fields.Selection(string="La pieza cumple con las dimensiones critícas.",selection=[("si","SI"),
                                         ("no","NO"),("na","NA")],default="na")
    #Seguridad
    filos = fields.Selection(string="Tiene filos.",selection=[("si","SI"),
                                         ("no","NO"),("na","NA")],default="na")
    tuercas = fields.Selection(string="Tuercas Apretadas.",selection=[("si","SI"),
                                         ("no","NO"),("na","NA")],default="na")

    #Adicional
    etiqueta_mexico = fields.Selection(string='La etiqueta "Hecho en México" esta visible en los 4 lados.', selection=[("si","SI"),
                                         ("no","NO"),("na","NA")],default="na" )
    empaque = fields.Selection(string='El empaque cubre de golpes y rayones toda la pieza.',selection=[("si","SI"),
                                         ("no","NO"),("na","NA")],default="na")

    aprobada = fields.Boolean(string="Pieza Aprobada:")
    motivo_rechazo = fields.Text(string="Motivo del Rechazo:")


