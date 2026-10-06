/** @odoo-module **/
import { Component, onWillStart, useState } from "@odoo/owl";

export class DialogMaquinados extends Component {
    static props = ["cerrar", "orden", "version"];

    setup() {

        this.state = useState({
            maquinados: [],
            showPDF: false,
            currentPDF: "",
        });
        onWillStart(async () => {
            await this.cargarMaquinados();
        });
    }

    async mostrarPDF(nombre) {
        this.state.showPDF = true;
        const response = await fetch("/seguimiento/po_pdf", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                nombre: nombre,
                orden_trabajo: this.props.orden,
                version: this.props.version,
            }),
        });
        const data = await response.json();
        this.state.currentPDF = data.result.pdf;
    }

    closePDF() {
        this.state.showPDF = false;
    }

    async cargarMaquinados() {
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
        this.state.maquinados = data.result.map((item) => ({ 'index': index++, ...item }));
    }
}
DialogMaquinados.template = "dtm_procesos.dialog_maquinados_template";
