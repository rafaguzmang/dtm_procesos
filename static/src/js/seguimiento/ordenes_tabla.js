/** @odoo-module **/

import { Component, onWillStart, useState, onMounted,onWillUnmount } from "@odoo/owl";
import { DialogMateriales } from "./pantallas_dialogo/dialog_materiales";
import { DialogCorteLaser } from "./pantallas_dialogo/dialog_corte_laser";
import { DialogMaquinados } from "./pantallas_dialogo/dialog_maquinados";
import { useService } from "@web/core/utils/hooks";

export class Ordenes extends Component{
    static components = {DialogMateriales, DialogCorteLaser, DialogMaquinados};
    setup(){
        this.state = useState({
            tabla:[],
            filtro_tabla:[],
            clientes_tabla:[],

            //Dialog corte laser
            corte_laser_dialog:false,
            
            //Dialog materiales
            materiales_dialog:false,

            //Dialog maquinados
            maquinados_dialog:false,

            // Variables para pasar a los diálogos
            orden_actual:'',
            version_actual:'',

        })
        this.busService = useService("bus_service")
        this.onBusNotification = this.onBusNotification.bind(this);

        onWillStart(async () => {
            await this.cargarTabla();          

        });

        onMounted(()=>{
            this.cargarTabla();
        });

        onWillUnmount(() => {
        });
    }

    onBusNotification(notifications) {
        console.log("Paquete recibido del bus:", notifications);
        console.log("notifications.detail",notifications.detail[0].payload.mensaje);
        this.cargarTabla();
    }
    // Función para obtener los maquinados
    maquinadosFunc = (orden,version)=>{        
        this.state.maquinados_dialog = true;
        this.state.orden_actual = orden;
        this.state.version_actual = version;
    }

    // Función para cerrar el diálogo de maquinados
    cerrarDialogoMaquinados = () => {
        this.state.maquinados_dialog = false;
    };
    // Función para obtener los cortes laser
    corteLaserFunc = (orden,version)=>{
        this.state.corte_laser_dialog = true;
        this.state.orden_actual = orden;
        this.state.version_actual = version;
    }
    // Función para cerrar el diálogo de corte laser
    cerrarDialogoCorteLaser = () => {
        this.state.corte_laser_dialog = false;
    }

    // Función para obtener todos los materiales en el cuadro de diálogo
    materialesFunc = (orden,version)=>{
        this.state.materiales_dialog = true;
        this.state.orden_actual = orden;
        this.state.version_actual = version;
    }
    // Función para cerrar el diálogo de materiales
    cerrarDialogoMateriales = () => {
        this.state.materiales_dialog = false;
    };
    // Cargar datos para la tabla de órdenes de producción
    async cargarTabla(){
        const response = await fetch("/seguimiento_procesos");
        const data = await response.json();
        let num = 0;
        // Se agrega un número de fila a cada registro para renderizar en la tabla
        const records = data.map(row => ({num:num++,...row}));
        this.state.tabla = records;
        this.state.filtro_tabla = records;       
        const clientes_list = records.map(record => record.cliente );
        const clientes_set = new Set(clientes_list);
        this.state.clientes_tabla = [...clientes_set]
    }

    //--------------------------- Filtro de búsqueda para la tabla----------------------------------------

    // Filtro por número de cotización
    cotizacionFiltro(event){
        const cotizacion = event.target.value;
        const po = event.target.closest('tr').querySelector('[name=po_filtro]').value??'';
        const maquinado = event.target.closest('tr').querySelector('[name=maquinados_filtro]').value??'';
        const corte = event.target.closest('tr').querySelector('[name=corte_filtro]').value??'';
        const material = event.target.closest('tr').querySelector('[name=material_filtro]').value??'';
        const nesteo = event.target.closest('tr').querySelector('[name=nesteo_filtro]').value??'';
        const fecha = event.target.closest('tr').querySelector('[name="fecha_filtro"]').value??'';
        const cliente = event.target.closest('tr').querySelector('[name=cliente_filtro]').value??'';
        const descripcion = event.target.closest('tr').querySelector('[name=descripcion_filtro]').value??'';
        const terminado = event.target.closest('tr').querySelector('[name=terminado_filtro]').value??'';
        this.filtroGeneral(cliente,descripcion,fecha,nesteo,material,corte,maquinado,po,terminado,cotizacion)
    }

    // Filtro pora saber si la orden ya fué terminada o sigue en porceso
    terminadoFiltro(event){
        const terminado = event.target.value;
        const po = event.target.closest('tr').querySelector('[name=po_filtro]').value??'';
        const maquinado = event.target.closest('tr').querySelector('[name=maquinados_filtro]').value??'';
        const corte = event.target.closest('tr').querySelector('[name=corte_filtro]').value??'';
        const material = event.target.closest('tr').querySelector('[name=material_filtro]').value??'';
        const nesteo = event.target.closest('tr').querySelector('[name=nesteo_filtro]').value??'';
        const fecha = event.target.closest('tr').querySelector('[name="fecha_filtro"]').value??'';
        const cliente = event.target.closest('tr').querySelector('[name=cliente_filtro]').value??'';
        const descripcion = event.target.closest('tr').querySelector('[name=descripcion_filtro]').value??'';
        const cotizacion =  event.target.closest('tr').querySelector('[name=cotizacion_filtro]').value??'';
        this.filtroGeneral(cliente,descripcion,fecha,nesteo,material,corte,maquinado,po,terminado,cotizacion)
    }

    // Filtro por po
    poFiltro(event){
        const po = event.target.value;
        const maquinado = event.target.closest('tr').querySelector('[name=maquinados_filtro]').value??'';
        const corte = event.target.closest('tr').querySelector('[name=corte_filtro]').value??'';
        const material = event.target.closest('tr').querySelector('[name=material_filtro]').value??'';
        const nesteo = event.target.closest('tr').querySelector('[name=nesteo_filtro]').value??'';
        const fecha = event.target.closest('tr').querySelector('[name="fecha_filtro"]').value??'';
        const cliente = event.target.closest('tr').querySelector('[name=cliente_filtro]').value??'';
        const descripcion = event.target.closest('tr').querySelector('[name=descripcion_filtro]').value??'';
        const terminado = event.target.closest('tr').querySelector('[name=terminado_filtro]').value??'';
        const cotizacion =  event.target.closest('tr').querySelector('[name=cotizacion_filtro]').value??'';
        this.filtroGeneral(cliente,descripcion,fecha,nesteo,material,corte,maquinado,po,terminado,cotizacion)
    }
    // Filtro por maquinados
    maquinadosFiltro(event){
        const maquinado = event.target.value;
        const corte = event.target.closest('tr').querySelector('[name=corte_filtro]').value??'';
        const material = event.target.closest('tr').querySelector('[name=material_filtro]').value??'';
        const nesteo = event.target.closest('tr').querySelector('[name=nesteo_filtro]').value??'';
        const fecha = event.target.closest('tr').querySelector('[name="fecha_filtro"]').value??'';
        const cliente = event.target.closest('tr').querySelector('[name=cliente_filtro]').value??'';
        const descripcion = event.target.closest('tr').querySelector('[name=descripcion_filtro]').value??'';
        const po = event.target.closest('tr').querySelector('[name=po_filtro]').value??'';
        const terminado = event.target.closest('tr').querySelector('[name=terminado_filtro]').value??'';
        const cotizacion =  event.target.closest('tr').querySelector('[name=cotizacion_filtro]').value??'';
        this.filtroGeneral(cliente,descripcion,fecha,nesteo,material,corte,maquinado,po,terminado,cotizacion)
    }

    // Filtro por cortes
    corteFiltro(event){
        const corte = event.target.value;
        const material = event.target.closest('tr').querySelector('[name=material_filtro]').value??'';
        const nesteo = event.target.closest('tr').querySelector('[name=nesteo_filtro]').value??'';
        const fecha = event.target.closest('tr').querySelector('[name="fecha_filtro"]').value??'';
        const cliente = event.target.closest('tr').querySelector('[name=cliente_filtro]').value??'';
        const descripcion = event.target.closest('tr').querySelector('[name=descripcion_filtro]').value??'';
        const maquinado = event.target.closest('tr').querySelector('[name=maquinados_filtro]').value??'';
        const po = event.target.closest('tr').querySelector('[name=po_filtro]').value??'';
        const terminado = event.target.closest('tr').querySelector('[name=terminado_filtro]').value??'';
        const cotizacion =  event.target.closest('tr').querySelector('[name=cotizacion_filtro]').value??'';
        this.filtroGeneral(cliente,descripcion,fecha,nesteo,material,corte,maquinado,po,terminado,cotizacion)
    }

    // Filtro por materiales
    materialFiltro(event){
        const material = event.target.value;
        const nesteo = event.target.closest('tr').querySelector('[name=nesteo_filtro]').value??'';
        const fecha = event.target.closest('tr').querySelector('[name="fecha_filtro"]').value??'';
        const cliente = event.target.closest('tr').querySelector('[name=cliente_filtro]').value??'';
        const descripcion = event.target.closest('tr').querySelector('[name=descripcion_filtro]').value??'';
        const corte = event.target.closest('tr').querySelector('[name=corte_filtro]').value??'';
        const maquinado = event.target.closest('tr').querySelector('[name=maquinados_filtro]').value??'';
        const po = event.target.closest('tr').querySelector('[name=po_filtro]').value??'';
        const terminado = event.target.closest('tr').querySelector('[name=terminado_filtro]').value??'';
        const cotizacion =  event.target.closest('tr').querySelector('[name=cotizacion_filtro]').value??'';
        this.filtroGeneral(cliente,descripcion,fecha,nesteo,material,corte,maquinado,po,terminado,cotizacion)
    }
    // Filtro  por nesteo
    nesteoFiltro(event){
        const nesteo = event.target.value;
        const fecha = event.target.closest('tr').querySelector('[name="fecha_filtro"]').value??'';
        const cliente = event.target.closest('tr').querySelector('[name=cliente_filtro]').value??'';
        const descripcion = event.target.closest('tr').querySelector('[name=descripcion_filtro]').value??'';
        const material = event.target.closest('tr').querySelector('[name=material_filtro]').value??'';
        const corte = event.target.closest('tr').querySelector('[name=corte_filtro]').value??'';
        const maquinado = event.target.closest('tr').querySelector('[name=maquinados_filtro]').value??'';
        const po = event.target.closest('tr').querySelector('[name=po_filtro]').value??'';
        const terminado = event.target.closest('tr').querySelector('[name=terminado_filtro]').value??'';
        const cotizacion =  event.target.closest('tr').querySelector('[name=cotizacion_filtro]').value??'';
        this.filtroGeneral(cliente,descripcion,fecha,nesteo,material,corte,maquinado,po,terminado,cotizacion)
    }
    // Filtro por fecha
    fechaFiltro(event){
        const fecha = event.target.value;
        const cliente = event.target.closest('tr').querySelector('[name=cliente_filtro]').value??'';
        const descripcion = event.target.closest('tr').querySelector('[name=descripcion_filtro]').value??'';
        const nesteo = event.target.closest('tr').querySelector('[name=nesteo_filtro]').value??'';
        const material = event.target.closest('tr').querySelector('[name=material_filtro]').value??'';
        const corte = event.target.closest('tr').querySelector('[name=corte_filtro]').value??'';
        const maquinado = event.target.closest('tr').querySelector('[name=maquinados_filtro]').value??'';
        const po = event.target.closest('tr').querySelector('[name=po_filtro]').value??'';
        const terminado = event.target.closest('tr').querySelector('[name=terminado_filtro]').value??'';
        const cotizacion =  event.target.closest('tr').querySelector('[name=cotizacion_filtro]').value??'';
        this.filtroGeneral(cliente,descripcion,fecha,nesteo,material,corte,maquinado,po,terminado,cotizacion)
    }
    // Filtro por descripción
    descripcionFiltro(event){
        const descripcion = (event.target.value).toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
        const cliente = event.target.closest('tr').querySelector('[name=cliente_filtro]').value??'';
        const fecha = event.target.closest('tr').querySelector('[name="fecha_filtro"]').value??'';
        const nesteo = event.target.closest('tr').querySelector('[name=nesteo_filtro]').value??'';
        const material = event.target.closest('tr').querySelector('[name=material_filtro]').value??'';
        const corte = event.target.closest('tr').querySelector('[name=corte_filtro]').value??'';
        const maquinado = event.target.closest('tr').querySelector('[name=maquinados_filtro]').value??'';
        const po = event.target.closest('tr').querySelector('[name=po_filtro]').value??'';
        const terminado = event.target.closest('tr').querySelector('[name=terminado_filtro]').value??'';
        const cotizacion =  event.target.closest('tr').querySelector('[name=cotizacion_filtro]').value??'';
        this.filtroGeneral(cliente,descripcion,fecha,nesteo,material,corte,maquinado,po,terminado,cotizacion)
    }
    // Filtro de busqueda por cliente
    clienteFiltro = (event) => {
        const cliente = event.target.value;
        const descripcion = event.target.closest('tr').querySelector('[name=descripcion_filtro]').value??''
        const fecha = event.target.closest('tr').querySelector('[name="fecha_filtro"]').value??'';
        const nesteo = event.target.closest('tr').querySelector('[name=nesteo_filtro]').value??'';
        const material = event.target.closest('tr').querySelector('[name=material_filtro]').value??'';
        const corte = event.target.closest('tr').querySelector('[name=corte_filtro]').value??'';
        const maquinado = event.target.closest('tr').querySelector('[name=maquinados_filtro]').value??'';
        const po = event.target.closest('tr').querySelector('[name=po_filtro]').value??'';
        const terminado = event.target.closest('tr').querySelector('[name=terminado_filtro]').value??'';
        const cotizacion =  event.target.closest('tr').querySelector('[name=cotizacion_filtro]').value??'';
        this.filtroGeneral(cliente,descripcion,fecha,nesteo,material,corte,maquinado,po,terminado,cotizacion)
    }

    // Filtro general
    filtroGeneral(cliente,descripcion,fecha,nesteo,material,corte,maquinado,po,terminado,cotizacion){
        let tabla = this.state.filtro_tabla;
        if(cliente){//Busca por cliente            
            tabla = tabla.filter(record => record.cliente == cliente);
        }     
        if(descripcion){//Busca por descripción
            tabla = tabla.filter(record => record.producto.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").includes(descripcion));
        }
        if (fecha) {//Busca por fecha
            const fechaInput = new Date(fecha);
            tabla = tabla.filter(record => {
                const [dia, mes, anio] = record.fecha_entrega.split("/");
                const fechaString = new Date(`${anio}-${mes}-${dia}`);
                return fechaString.getTime() === fechaInput.getTime();
            });
        }
        if (nesteo) {//Busca por nesteo            
            const result = nesteo === 'si'?'100%':'0%'; 
            console.log(result);            
            tabla = tabla.filter(record => record.nesteo === result);
        }
        if (material){           
            if (material === 'completo'){
                tabla = tabla.filter(record => record.compra_material === "100%");
            }else if(material === 'vacio'){
                tabla = tabla.filter(record => record.compra_material === "0%");
            }else{
                tabla = tabla.filter(record => parseInt(record.compra_material.replace('%','')) > 0 && parseInt(record.compra_material.replace('%','')) < 100);
            }            
        }
        if (corte){           
            if (corte === 'completo'){
                tabla = tabla.filter(record => record.corte === "100%");
            }else if(corte === 'vacio'){
                tabla = tabla.filter(record => record.corte === "0%");
            }else if(corte === 'na'){
                tabla = tabla.filter(record => record.corte === "N/A");
            }else{
                tabla = tabla.filter(record => parseInt(record.corte.replace('%','')) > 0 && parseInt(record.corte.replace('%','')) < 100);
            }            
        }
        if (maquinado){           
            if (maquinado === 'completo'){
                tabla = tabla.filter(record => record.maquinado === "100%");
            }else if(maquinado === 'vacio'){
                tabla = tabla.filter(record => record.maquinado === "0%");
            }else if(maquinado === 'na'){
                tabla = tabla.filter(record => record.maquinado === "N/A");
            }else{
                tabla = tabla.filter(record => parseInt(record.maquinado.replace('%','')) > 0 && parseInt(record.maquinado.replace('%','')) < 100);
            }            
        }
        if (po){
            tabla = tabla.filter(record => record.po == po);
        }
        if (cotizacion){
            tabla = tabla.filter(record => record.cotizacion == cotizacion);
        }
        if (terminado){
            const result = terminado === 'si'?'100%':'0%'; 
            console.log(result);            
            tabla = tabla.filter(record => record.terminado === result);
        }
        this.state.tabla = tabla;
    }

    // Filtro por la busqueda de número de orden
    ordenFiltro = (event)=>{
        const orden = event.target.value;
        this.state.tabla = this.state.filtro_tabla.filter(record => record.orden == orden);
        this.state.tabla = event.target.value == '' ? this.state.filtro_tabla:this.state.tabla;
    }

    // Filtro de búsqueda por tipo de orden
    tipoOrdenFiltro = (event) =>{
        const tipo = event.target.value;
        this.state.tabla = this.state.filtro_tabla.filter(record => record.tipo == tipo.toUpperCase());
        this.state.tabla = event.target.value == '' ? this.state.filtro_tabla:this.state.tabla;
    }
}

Ordenes.template = "dtm_procesos.ordenes_tabla"
