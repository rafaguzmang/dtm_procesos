/** @odoo-module **/

import { Component, useState, useRef, onMounted, onWillUnmount, onWillStart   } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

//console.log("indicacor de Procesos");

export class Seguimiento extends Component {
    setup(){
        this.state = useState({
            tabla:[],
            total:0,
        })

        onWillStart(async() => {
             await this.dataFetch();
        });

        onMounted(() => {

            try {

                this.intervalId = setInterval(() => {
                   this.dataFetch();
                }, 5000); // 5000ms = 5 segundos


            }catch (error){
                console.log('Error al hacer el fetch: ',error);
            }

        });

    }

     async dataFetch() {

             const response = await fetch('/seguimiento_procesos',{
                        method:'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-Requested-With': 'XMLHttpRequest'
                        },
                        body:JSON.stringify({})
                    })

            const data = await response.json();
            this.state.tabla = data.result;
            this.state.tabla = this.state.tabla.map(row =>(
                {
                    ...row,
                    dias: (((new Date(row.fecha_rel) - new Date().getTime()) / (1000 * 60 * 60 * 24)) + 1).toFixed(0),
                    status: row.status === 'corte'?'Corte':
                            row.status === 'revision'?'Revisión FAI':
                            row.status === 'doblado'?'Doblado':
                            row.status === 'soldadura'?'Soldadura':
                            row.status === 'maquinado'?'Maquinado':
                            row.status === 'pintura'?'Pintura':
                            row.status === 'ensamble'?'Ensamble':
                            row.status === 'calidad'?'Calidad':
                            row.status === 'instalacion'?'Instalación':
                            row.status === ''?'':null,
                }
            ));
            this.state.tabla.sort((a,b)=> a.dias - b.dias)
            this.state.total = this.state.tabla.length
            console.log('Respuesta:', this.state.tabla);
        }
}

Seguimiento.template = "dtm_procesos.seguimiento";

registry.category("actions").add('dtm_procesos.seguimiento', Seguimiento);




