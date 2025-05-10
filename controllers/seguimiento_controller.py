from odoo import http
from odoo.http import request

class ProcesosController(http.Controller):

    @http.rooute('/seguimiento_procesos', type='json', auth='public')
    def ordenes_trabajo(self, **kwargs):

        return {'mensaje':'Hola desde el backend','datos':kwargs}