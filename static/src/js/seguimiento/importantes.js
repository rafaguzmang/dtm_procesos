    /** @odoo-module **/
    import { Component, useState, onWillStart, onWillUnmount,onMounted  } from "@odoo/owl";
    import { DialogMateriales } from "./pantallas_dialogo/dialog_materiales";
    import { DialogCorteLaser } from "./pantallas_dialogo/dialog_corte_laser";
    import { DialogMaquinados } from "./pantallas_dialogo/dialog_maquinados";
    import { DialogMaterialesLiberar } from "./pantallas_dialogo/dialog_materiales_liberar";
    import { DialogCompraMaterial } from "./pantallas_dialogo/dialog_compra_material";

    export class Importantes extends Component {
        static components = { DialogMateriales, DialogCorteLaser, DialogMaquinados, DialogMaterialesLiberar, DialogCompraMaterial};
        setup() {
            let interval = null;
            this.state = useState({
                importantes: [],
                importante_total: 0,
                // Ventanas de diálogo
                materiales_dialog: false,
                corte_dialog: false,
                maquinados_dialog: false,
                liberar_materiales_dialog: false,
                compra_materiales_dialog: false,

                // Datos para pasar a los diálogos
                orden_actual: null,
                version_actual: null,
            });

            onWillStart(async () => {
               await this.loadImportantes();
            });

           onMounted(() => {
               interval = setInterval(() => {
                   this.loadImportantes();
               }, 5000);
           });

           onWillUnmount(() => {
               clearInterval(interval);
           });
        }

        async loadImportantes() {
            const response = await fetch("/seguimiento_procesos");
            const data = await response.json();
            let num = 0;
            const result  = data.map(row=>({'id':num++,...row}))
            this.state.importantes = result.filter(item => item.prioridad);
            this.state.importantes = this.state.importantes.sort((a,b) => b.prioridad - a.prioridad);
            this.state.importante_total = this.state.importantes.length;
        };

        // Función para obtener todos los materiales faltantes de comprar
        abrirDialogoCompra = (orden,version)=>{
            this.state.compra_materiales_dialog = true;
            this.state.orden_actual = orden;
            this.state.version_actual = version;
        };
        // Función para cerrar el diálogo de materiales de comprar
        cerrarDialogoCompra = () => {
            this.state.compra_materiales_dialog = false;
        };

        // Función para obtener todos los materiales faltantes para autorizar
        abrirDialogLiberar = (orden,version)=>{
            this.state.liberar_materiales_dialog = true;
            this.state.orden_actual = orden;
            this.state.version_actual = version;
        };
        // Función para cerrar el diálogo de materiales para autorizar
        cerrarDialogLiberar = () => {
            this.state.liberar_materiales_dialog = false;
        };
        // Función para obtener todos los materiales en el cuadro de diálogo
        abrirDialogoMateriales = (orden,version)=>{
            this.state.materiales_dialog = true;
            this.state.orden_actual = orden;
            this.state.version_actual = version;
        }
        // Función para cerrar el diálogo de materiales
        cerrarDialogoMateriales = () => {
            this.state.materiales_dialog = false;
        };

        // Función para obtener todos los cortes en el cuadro de diálogo
        abrirDialogoCorte = (orden,version)=>{
            this.state.corte_dialog = true;
            this.state.orden_actual = orden;
            this.state.version_actual = version;
        }
        // Función para cerrar el diálogo de materiales
        cerrarDialogoCorte = () => {
            this.state.corte_dialog = false;
        };

        // Función para obtener todos los maquinados en el cuadro de diálogo
        abrirDialogoMaquinados = (orden,version)=>{
            this.state.maquinados_dialog = true;
            this.state.orden_actual = orden;
            this.state.version_actual = version;
        }
        // Función para cerrar el diálogo de materiales
        cerrarDialogoMaquinados = () => {
           this.state.maquinados_dialog = false;
       };
     }

    Importantes.template = "dtm_procesos.importantes";
