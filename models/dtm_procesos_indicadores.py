from odoo import api,models,fields
from datetime import datetime

class Indicadores(models.Model):
    _name = 'dtm.procesos.indicadores'
    _description = 'Modulo para llevar los xml de producción'
    # _rec_name = 'mes'

    no_month = fields.Integer()
    mes = fields.Char(string='Mes')
    ordenes = fields.Integer(string="Ordenes")
    en_tiempo = fields.Integer(string="En tiempo")
    tarde = fields.Integer(string="Con Retardo")
    porcentaje = fields.Float(string="%")

    def get_view(self, view_id=None, view_type='form', **options):
        res = super(Indicadores, self).get_view(view_id, view_type, **options)

        for month in range(1, 13):
            if month <= int(datetime.today().strftime("%m")):
                # Busca las cotizaciones del mes actual y del mes pasado
                self.env.cr.execute(
                    " SELECT date_rel, date_terminado,ot_number FROM dtm_facturado_odt WHERE EXTRACT(MONTH FROM date_rel) = " + str(month) +
                    " AND EXTRACT(YEAR FROM date_rel) = " + datetime.today().strftime("%Y") + ";")
                get_proceso = self.env.cr.fetchall()

                tiempo = 0
                tarde = 0
                mes = 0
                if get_proceso:
                    # Obtiene todos las ordenes con fecha de entraga del mes a consultar
                    for cotizacion in get_proceso:
                        if int(cotizacion[0].strftime("%j")) >= (int(cotizacion[1].strftime("%j")) if cotizacion[1] else 1000):
                            tiempo += 1
                        else:
                            tarde += 1

                        mes = cotizacion[0].strftime("%B").capitalize()

                # Si el mes existe lo actualiza si no lo crea
                get_this = self.env['dtm.procesos.indicadores'].search([('no_month', '=', month)])
                if get_this:
                    get_this.write({
                        'no_month':month,
                        'mes':mes if mes != 0 else datetime.today().strftime("%B").capitalize()  ,
                        'ordenes':len(get_proceso),
                        'en_tiempo':tiempo,
                        'tarde':tarde,
                        'porcentaje':(tiempo*100)/max(len(get_proceso),1),
                    })
                else:
                    get_this.create({
                        'no_month':month,
                        'mes':mes,
                        'ordenes':len(get_proceso),
                        'en_tiempo':tiempo,
                        'tarde':tarde,
                        'porcentaje':(tiempo*100)/max(len(get_proceso),1),
                    })
        return res