from odoo import api,models,fields
import re

class Proceso(models.Model):
    _name = "dtm.proceso"
    _description = "Modulo para indicar el status de la ODT o NPI"

    status = fields.Selection(string="Estatus",selection=[("corte","Corte"),("doblado","Doblado"),("soldadura","Soldadura"),("lavado","Lavado"),("pintura","Pintura"),("ensamble","Ensamble"),("terminado","Terminado")])

    sequence = fields.Integer()
    ot_number = fields.Char(string="NÚMERO",readonly=True)
    tipe_order = fields.Char(string="TIPO",readonly=True)
    name_client = fields.Char(string="CLIENTE",readonly=True)
    product_name = fields.Char(string="NOMBRE DEL PRODUCTO",readonly=True)
    date_in = fields.Date(string="FECHA DE ENTRADA", readonly=True)
    po_number = fields.Char(string="PO",readonly=True)
    date_rel = fields.Date(string="FECHA DE ENTREGA",readonly=True)
    version_ot = fields.Integer(string="VERSIÓN OT",readonly=True)
    color = fields.Char(string="COLOR",readonly=True)
    cuantity = fields.Integer(string="CANTIDAD",readonly=True)
    materials_ids = fields.Many2many("dtm.proceso.materials",readonly=True)
    firma = fields.Char(string="Firma", readonly = True)

    planos = fields.Boolean(string="Planos",default=False,readonly=True)
    nesteos = fields.Boolean(string="Nesteos",default=False,readonly=True)

    rechazo_id = fields.Many2many("dtm.proceso.rechazo")

    anexos_id = fields.One2many("dtm.proceso.anexos","model_id")
    cortadora_id = fields.One2many("dtm.proceso.cortadora","model_id")
    tubos_id = fields.One2many("dtm.proceso.tubos","model_id")

    #---------------------Resumen de descripción------------

    description = fields.Text(string= "DESCRIPCIÓN",placeholder="RESUMEN DE DESCRIPCIÓN")

    notes = fields.Text()


    # def get_view(self, view_id=None, view_type='form', **options):
    #     res = super(Proceso,self).get_view(view_id, view_type,**options)
    #     get_odt = self.env['dtm.odt'].search([])
    #     get_npi = self.env['dtm.npi'].search([])
    #     get_array = [get_odt,get_npi]
    #     for modulo in get_array:
    #
    #         for get in modulo:
    #             # print(get.ot_number,modulo,get.name_client)
    #             get_this = self.env['dtm.proceso'].search([("ot_number","=",get.ot_number),("tipe_order","=",get.tipe_order)])
    #             vals = {
    #                 "ot_number":get.ot_number,
    #                 "tipe_order":get.tipe_order,
    #                 "name_client":get.name_client,
    #                 "product_name":get.product_name,
    #                 "date_in":get.date_in,
    #                 "date_rel":get.date_rel,
    #                 "version_ot":get.version_ot,
    #                 "cuantity":get.cuantity,
    #                 "po_number":"N/A",
    #                 "description":get.description,
    #                 "planos":get.planos,
    #                 "nesteos":get.nesteos,
    #                 "notes":get.notes
    #
    #             }
    #             # print(get.ot_number,get.materials_ids)
    #
    #             if re.match(".*odt.*",str(modulo)):
    #                 vals["po_number"] = get.po_number
    #                 vals["color"] = get.color
    #             else:
    #                 vals["name_client"] = get.name_client.name
    #
    #             if get_this:
    #                 get_this.write(vals)
    #
    #             else:
    #                 get_this.create(vals)
    #
    #             lines = []
    #             for materi in get.materials_ids:
    #                 datos = {
    #                     "nombre":materi.nombre,
    #                     "medida":materi.medida,
    #                     "materials_cuantity":materi.materials_cuantity,
    #                     "materials_inventory":materi.materials_inventory,
    #                     "materials_required":materi.materials_required
    #                 }
    #                 if self.env['dtm.proceso.materials'].search([("nombre","=",materi.nombre),("medida","=",materi.medida),
    #                                                              ("materials_cuantity","=",materi.materials_cuantity),("materials_inventory","=",materi.materials_inventory),
    #                                                              ("materials_required","=",materi.materials_required)]):
    #                 # if materi.nombre ==
    #                     line = (1,get_this.id,datos)
    #                 else:
    #                     line = (0,get_this.id,datos)
    #                 lines.append(line)
    #
    #             get_this.materials_ids = lines
    #
    #             lines = []
    #             for materi in get.rechazo_id:
    #                 datos = {
    #                     "decripcion":materi.decripcion,
    #                     "fecha":materi.fecha,
    #                     "hora":materi.hora,
    #                     "firma":materi.firma
    #                 }
    #                 if self.env['dtm.proceso.rechazo'].search([("decripcion","=",materi.decripcion),("fecha","=",materi.fecha),
    #                                                              ("hora","=",materi.hora),("firma","=",materi.firma)]):
    #
    #                     line = (1,get_this.id,datos)
    #                 else:
    #                     line = (0,get_this.id,datos)
    #                 lines.append(line)
    #
    #             get_this.rechazo_id = lines
    #
    #             lines = []
    #             # for materi in get.anexos_id:
    #             #     datos = {
    #             #         "documentos":materi.documentos,
    #             #         "nombre":materi.nombre
    #             #     }
    #             #     if self.env['dtm.proceso.anexos'].search([("documentos","=",materi.documentos),("nombre","=",materi.nombre)]):
    #             #
    #             #         line = (1,get_this.id,datos)
    #             #     else:
    #             #         line = (0,get_this.id,datos)
    #             #     lines.append(line)
    #             #
    #             # get_this.anexos_id = lines
    #             #
    #             # lines = []
    #             # for materi in get.cortadora_id:
    #             #     datos = {
    #             #         "documentos":materi.documentos,
    #             #         "nombre":materi.nombre
    #             #     }
    #             #     if self.env['dtm.proceso.cortadora'].search([("documentos","=",materi.documentos),("nombre","=",materi.nombre)]):
    #             #
    #             #         line = (1,get_this.id,datos)
    #             #     else:
    #             #         line = (0,get_this.id,datos)
    #             #     lines.append(line)
    #             #
    #             # get_this.cortadora_id = lines
    #
    #             lines = []
    #             for materi in get.tubos_id:
    #                 datos = {
    #                     "documentos":materi.documentos,
    #                     "nombre":materi.nombre
    #                 }
    #                 if self.env['dtm.proceso.tubos'].search([("documentos","=",materi.documentos),("nombre","=",materi.nombre)]):
    #
    #                     line = (1,get_this.id,datos)
    #                 else:
    #                     line = (0,get_this.id,datos)
    #                 lines.append(line)
    #
    #             get_this.tubos_id = lines
    #
    #     return res


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

    decripcion = fields.Text(string="Descripción del Rechazo")
    fecha = fields.Date(string="Fecha")
    hora = fields.Char(string="Hora")
    firma = fields.Char(string="Firma")

class Documentos(models.Model):
    _name = "dtm.proceso.anexos"
    _description = "Guarda todos los planos de la orden de trabajo"

    model_id = fields.Many2one("dtm.proceso")
    documentos = fields.Binary()
    nombre = fields.Char()


class Cortadora(models.Model):
    _name = "dtm.proceso.cortadora"
    _description = "Guarda los nesteos del Radán"

    model_id = fields.Many2one("dtm.proceso")
    documentos = fields.Binary()
    nombre = fields.Char()

class Tubos(models.Model):
    _name = "dtm.proceso.tubos"
    _description = "Guarda los nesteos de la cortadora de tubos"

    model_id = fields.Many2one("dtm.proceso")
    documentos = fields.Binary()
    nombre = fields.Char()




