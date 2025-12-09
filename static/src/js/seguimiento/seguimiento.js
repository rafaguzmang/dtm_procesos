/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
// Componentes
import { Ordenes } from "./ordenes_tabla";
//import { Importantes } from "./importantes";
import { CorteLaser } from "./corte_laser";



export class Seguimiento extends Component {
//    static components = {Ordenes, Importantes, };
    static components = {Ordenes, CorteLaser};

}

Seguimiento.template = "dtm_procesos.seguimiento";

registry.category("actions").add('dtm_procesos.seguimiento', Seguimiento);




