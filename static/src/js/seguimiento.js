/** @odoo-module **/

import { Component, useState, useRef, onMounted, onWillUnmount, onWillStart   } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { DialogMateriales } from "./dialog_materiales";



export class Seguimiento extends Component {
    static components = { DialogMateriales };
    setup(){
        this.state = useState({
            completa:[],
            tabla:[],
            total:0,
            materiales:[],
            showDialogMateriales: false,
            dialogOrden: null,
            dialogMateriales:[],
            clientes:[],
            producto:[],
            disenador:[],
            status:[],
            orden:[],
            tipo:[]
        })

        onWillStart(async() => {
             await this.dataFetch();
        });

        onMounted(() => {

            try {

//                this.intervalId = setInterval(() => {
                   this.dataFetch();
//                }, 5000); // 5000ms = 5 segundos


            }catch (error){
                console.log('Error al hacer el fetch: ',error);
            }

        });
    }

    mostrarDialogo(orden) {

        const materialData = this.state.materiales.find(item => item.orden === orden);
        if (materialData) {
            this.state.dialogOrden = orden;
            this.state.dialogMateriales = materialData.materiales;
            this.state.showDialogMateriales = true;
        } else {
            console.error("No se encontraron materiales para la orden:", orden);
        }

    }

    async dataFetch() {

            const response_materiales = await fetch('/seguimiento_materiales',{
                method:'POST',
                headers:{
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body:JSON.stringify({})
            })

            const materiales_data = await response_materiales.json();
            this.state.materiales = materiales_data.result;
//            console.log('Materiales',materiales_data.result);


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
                    materiales_lista: materiales_data.result.filter(item => item.orden === row.orden).flatMap(item => item.materiales.map((mat, index) => ({
                    id: index + 1,
                    material: mat
                }))),
                }
            ));
//            console.log(this.state.tabla)
            this.state.tabla.sort((a,b)=> a.dias - b.dias);
            this.state.completa = this.state.tabla;
            this.state.total = this.state.tabla.length;
//            console.log('Respuesta:', this.state.tabla);
//            Obtenemos todos los clientes
            const clientes = new Set(this.state.tabla.map(row=> row.cliente));
            this.state.clientes = Array.from(clientes);
//            Obtenemos el nombre de todos los proyectos
            const producto = new Set(this.state.tabla.map(row=> row.producto));
            this.state.producto = Array.from(producto);
//            Obtenemos el nombre de los diseñadores
            const disenador = new Set(this.state.tabla.map(row=> row.disenador));
            this.state.disenador = Array.from(disenador);
//            Obtenemos el status de los proyectos
            const status = new Set(this.state.tabla.map(row=> row.status));
            this.state.status = Array.from(status);
//            Obtenemos los números de orden
            const orden = new Set(this.state.tabla.map(row=> row.orden));
            this.state.orden = Array.from(orden);
//            Obtenemos los tipos de orden que hay
            const tipo = new Set(this.state.tabla.map(row=> row.tipo));
            this.state.tipo = Array.from(tipo);
        }

    onClienteChange(ev) {
        const cliente = ev.target.value
        this.state.tabla = this.state.completa;
        if (cliente== 'Todo'){
            this.state.tabla = this.state.completa;
        }else{
            this.state.tabla = this.state.tabla.filter(row=> row.cliente == cliente);
        }
    }
    onProductoChange(ev) {
        const producto = ev.target.value
        this.state.tabla = this.state.completa;
        if (producto== 'Todo'){
            this.state.tabla = this.state.completa;
        }else{
            this.state.tabla = this.state.tabla.filter(row=> row.producto == producto);
        }
    }
    onDisenadorChange(ev) {
        const disenador = ev.target.value
        this.state.tabla = this.state.completa;

        if (disenador == 'Todo'){
            this.state.tabla = this.state.completa;
        }else{
             this.state.tabla = this.state.tabla.filter(row=> row.disenador == disenador);
        }
    }
    onStatusChange(ev) {
        const status = ev.target.value
        this.state.tabla = this.state.completa;
        if (status == 'Todo'){
            this.state.tabla = this.state.completa;
        }else{
            this.state.tabla = this.state.tabla.filter(row=> row.status == status);
        }
    }
    onOrdenChange(ev) {
        const orden = ev.target.value
        this.state.tabla = this.state.completa;
        if (orden == 'Todo'){
            this.state.tabla = this.state.completa;
        }else{
            this.state.tabla = this.state.tabla.filter(row=> row.orden == orden);
        }
    }
    onTipoChange(ev) {
        const tipo = ev.target.value
        this.state.tabla = this.state.completa;
        if (tipo == 'Todo'){
            this.state.tabla = this.state.completa;
        }else{
            this.state.tabla = this.state.tabla.filter(row=> row.tipo == tipo);
        }
    }
}

Seguimiento.template = "dtm_procesos.seguimiento";

registry.category("actions").add('dtm_procesos.seguimiento', Seguimiento);




