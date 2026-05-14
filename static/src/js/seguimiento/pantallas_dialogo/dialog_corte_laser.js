/** @odoo-module **/
import { Component, useState, onWillStart } from "@odoo/owl";

export class DialogCorteLaser extends Component {
    static props = [
        "cerrar",
        "orden",
        "version",
    ];
    setup() {
        this.state = useState({
            cortes_primera: [],
            cortes_segunda: [],
            pdf: null,
            showPDF: false,
        })

        onWillStart(async () => {
            this.descargarCorte();
        });
    }

    async openPDF(pdf) {
        this.state.pdf = pdf;
        this.state.showPDF = true;
    }

    async closePDF() {
        this.state.pdf = null;
        this.state.showPDF = false;
    }

    async descargarCorte() {
        const response = await fetch("/seguimiento_corte_laser", {
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
        const primera_tabla = data.result.filter(row => row.primera_pieza === true);
        const segunda_tabla = data.result.filter(row => row.primera_pieza === false);
        let index = 0;
        this.state.cortes_primera = primera_tabla.map(row => ({ 'index': index++, ...row }));
        index = 0;
        this.state.cortes_segunda = segunda_tabla.map(row => ({ 'index': index++, ...row }));
    }



}
DialogCorteLaser.template = "dtm_procesos.dialog_corte_laser_template";
