/** @odoo-module **/
import { Component, onWillStart, useState } from "@odoo/owl";

export class DialogMaquinados extends Component{
    static props = ["cerrar", "orden", "version"];

    setup(){

        this.state = useState({
            maquinados: [],
        });
        onWillStart(async () => {
            await this.cargarMaquinados();
        });        
    }

    async cargarMaquinados(){
        const response = await fetch("/seguimiento_maquinados", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                orden: this.props.orden,    
                version: this.props.version,
            }),
        });
        const data = await response.json();
        let index = 0;
        this.state.maquinados = data.result.map((item) => ({'index': index++, ...item}));
        console.log(data.result);
    }
}
DialogMaquinados.template = "dtm_procesos.dialog_maquinados_template";
