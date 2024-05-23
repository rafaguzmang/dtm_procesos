{
    "name":"Procesos",

    'version': '1.0',
    'author': "Rafael Guzmán",
    "description": "Modulo para el área de compras",
    "depends":["dtm_odt"],
    "data":[
        'security/ir.model.access.csv',
        #Views
        'views/dtm_proceso_views.xml',
        #Menú
        # 'views/dtm_menu.xml'

    ],
    'assets': {
    'web.assets_backend': [
        'dtm_procesos/static/src/css/kanban.css',
    ],
}
}

