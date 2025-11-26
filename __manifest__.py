{
    "name":"Procesos",

    'version': '1.0',
    'author': "Rafael Guzmán",
    "description": "Modulo para el área de compras",
    "depends":['base', 'mail',"dtm_odt",'web'],
    "data":[
        #Security
        'security/ir.model.access.csv',
        # 'security/res_groups.xml',
        # 'security/model_access.xml',
        #Views
        'views/dtm_proceso_views.xml',
        'views/dtm_procesos_liberacion_view.xml',
        'views/indicador_view.xml',
        'views/seguimiento_view.xml',

        #Menú
        'views/dtm_menu.xml',
        #Reports
        'reports/orden_de_trabajo.xml',
        'reports/lista_materiales.xml',
        #Script
        # 'static/xml/assets.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # CSS
            'dtm_procesos/static/src/css/styles.css',
            'dtm_procesos/static/src/css/ordene_tabla.css',
            'dtm_procesos/static/src/css/importantes.css',
            # JS
            'dtm_procesos/static/src/js/indicador.js',
            'dtm_procesos/static/src/js/seguimiento/seguimiento.js',
            'dtm_procesos/static/src/js/seguimiento/ordenes_tabla.js',
            'dtm_procesos/static/src/js/seguimiento/pantallas_dialogo/dialog_materiales.js',
            'dtm_procesos/static/src/js/seguimiento/pantallas_dialogo/dialog_corte_laser.js',
            'dtm_procesos/static/src/js/seguimiento/pantallas_dialogo/dialog_maquinados.js',
            'dtm_procesos/static/src/js/seguimiento/importantes.js',
            'dtm_procesos/static/src/js/seguimiento/corte_laser.js',

            # XML
            'dtm_procesos/static/src/xml/indicador.xml',
            'dtm_procesos/static/src/xml/seguimiento/seguimiento.xml',
            'dtm_procesos/static/src/xml/seguimiento/ordenes_tabla.xml',
            'dtm_procesos/static/src/xml/seguimiento/pantallas_dialogo/dialog_materiales_template.xml',
            'dtm_procesos/static/src/xml/seguimiento/pantallas_dialogo/dialog_corte_laser_template.xml',
            'dtm_procesos/static/src/xml/seguimiento/pantallas_dialogo/dialog_maquinados.xml',
            'dtm_procesos/static/src/xml/seguimiento/importantes.xml',
            'dtm_procesos/static/src/xml/seguimiento/corte_laser.xml',
            ],
    },
    'license': 'LGPL-3',
}
