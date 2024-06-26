{
    "name":"Procesos",

    'version': '1.0',
    'author': "Rafael Guzmán",
    "description": "Modulo para el área de compras",
    "depends":['base', 'mail',"dtm_odt",'web'],
    "data":[
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        #Views
        'views/dtm_proceso_views.xml',
        #Menú
        'views/dtm_menu.xml',
        #Reports
        'reports/orden_de_trabajo.xml',
        'reports/lista_materiales.xml',
        #Script
        # 'static/xml/assets.xml',
    ]
}

