from odoo import models,fields,api
from datetime import datetime

class PrimeraPieza(models.Model):
    _name = "dtm.procesos.liberacion.primera"
    _description = "Módulo con el formato de liberación de primeras piezas"
    
    model_id = fields.Many2one("dtm.proceso")
    fecha_revision = fields.Date(default= datetime.today(),readonly=True)
    aprobacion = fields.Char(string='Aprobación', default=lambda self: self.env.user.partner_id.name,readonly=True)

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