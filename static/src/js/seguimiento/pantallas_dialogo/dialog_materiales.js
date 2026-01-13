/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";

export class DialogMateriales extends Component{
    static props = [
        "cerrar",
        "orden",
        "version",
    ];
    setup(){
        this.state = useState({
            materiales: [],
        })

        onWillStart(async () => {
            await this.cargarMateriales();
        })
    }

    async cargarMateriales(){
        const response = await fetch("/seguimiento_materiales", {
            method: "POST",         
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(
                {
                    'orden': this.props.orden,
                    'version': this.props.version,
                }),
        });
        const data = await response.json();
        let num = 0;
        this.state.materiales = data.result.map(item => ({'num':num++,...item}));        
    }
}
DialogMateriales.template = "dtm_procesos.dialog_materiales_template";


