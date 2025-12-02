/** @odoo-module **/
import { Component, onWillStart } from "@odoo/owl";

export class DialogCompraMaterial extends Component {
    static props = ["orden", "version", "cerrar"];
    setup() {
        this.state = {
            materiales:[],
        }

        onWillStart(async () => {
            await this.descargarMateriales();
        });

    }

    async descargarMateriales(){
        const response = await fetch("/compra_material", {
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
        console.log("Materiales",data.result);
        let index = 0;
        this.state.materiales = data.result.map(row=>({'index':index++,...row}));
    }
}

DialogCompraMaterial.template = "dtm_procesos.dialog_compra_material"