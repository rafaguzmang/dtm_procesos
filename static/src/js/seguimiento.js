/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

//console.log("indicacor de Procesos");

export class Seguimiento extends Component {
    setup(){

//        onMounted(async () => {
//            const response = await fetch('/',{
//                method:'Post',
//                header:{
//                    'Content-Type': 'application/json',
//                    'X-Requested-With': 'XMLHttpRequest'
//                },
//                body:JSON.stringify({
//                    parametro1:'valor1',
//                    parametro2:'valor2'
//                })
//            })
//
//        });
//        const data = await response.json();
//        console.log('Respuesta:', data)


    }
}

Seguimiento.template = "dtm_procesos.seguimiento";

registry.category("actions").add('dtm_procesos.seguimiento', Seguimiento);




