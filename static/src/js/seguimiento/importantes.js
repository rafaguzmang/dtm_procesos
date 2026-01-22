    /** @odoo-module **/
    import { Component, useState, onWillStart, onWillUnmount,onMounted  } from "@odoo/owl";
    import { useService } from "@web/core/utils/hooks";
    import { DialogMateriales } from "./pantallas_dialogo/dialog_materiales";
    import { DialogCorteLaser } from "./pantallas_dialogo/dialog_corte_laser";
    import { DialogMaquinados } from "./pantallas_dialogo/dialog_maquinados";
    import { DialogMaterialesLiberar } from "./pantallas_dialogo/dialog_materiales_liberar";
    import { DialogCompraMaterial } from "./pantallas_dialogo/dialog_compra_material";

    export class Importantes extends Component {
        static components = { DialogMateriales, DialogCorteLaser, DialogMaquinados, DialogMaterialesLiberar, DialogCompraMaterial};
        setup() {
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
            this.busService = useService("bus_service");
            this.onBusNotification = this.onBusNotification.bind(this);

            onWillStart(async () => {
                await this.loadImportantes();
                this.busService.addChannel("canal_ots");
                this.busService.addEventListener("notification", this.onBusNotification);
                this.busService.addChannel("canal_compras");
                this.busService.addEventListener("notification", this.onBusNotification);
                this.busService.addChannel("canal_corte");
                this.busService.addEventListener("notification", this.onBusNotification);
                this.busService.addChannel("canal_maquinados");
                this.busService.addEventListener("notification", this.onBusNotification);
                this.busService.addChannel("canal_manufactura");
                this.busService.addEventListener("notification", this.onBusNotification);
            });

           onMounted(() => {
               this.loadImportantes();
           });

           onWillUnmount(() => {
              this.busService.removeEventListener('notification', this.onBusNotification);
           });
        }

        onBusNotification(notifications){
            console.log("Paquete recibido del bus");
            console.log("nofications.detail");
            this.loadImportantes();
        }

        async loadImportantes() {
            const response = await fetch("/seguimiento_importantes");
            const data = await response.json();
//            console.log(data)
            this.state.importantes = data;
        };

        getMondayOfWeek(year, week) {
            try {
                // Validaciones duras
                const y = parseInt(year, 10);
                const w = parseInt(week, 10);
                if (!Number.isInteger(y) || !Number.isInteger(w) || w < 1 || w > 53) {
                    return "Semana inválida";
                }

                // ISO: el jueves de la semana 1 define el año de la semana
                // Paso 1: jueves de la semana 'w'
                const fourthJan = new Date(Date.UTC(y, 0, 4));            // 4 de enero (UTC)
                const dayOfWeek = fourthJan.getUTCDay() || 7;             // 1..7 (lunes..domingo)
                const isoWeek1Monday = new Date(fourthJan);               // lunes de la semana 1
                isoWeek1Monday.setUTCDate(fourthJan.getUTCDate() - (dayOfWeek - 1));

                // Paso 2: lunes de la semana w
                const monday = new Date(isoWeek1Monday);
                monday.setUTCDate(isoWeek1Monday.getUTCDate() + (w - 1) * 7);

                // Validación final
                if (isNaN(monday.getTime())) {
                    return "Fecha inválida";
                }

                // Extraer día y mes (en local, pero desde UTC para evitar DST)
                const dayNumber = monday.getUTCDate();
                const monthName = monday.toLocaleString('es-MX', { month: 'long', timeZone: 'UTC' });

                return `${dayNumber} de ${monthName}`; // "22 de diciembre"
            } catch (e) {
                // Previene que OWL se caiga silenciosamente
                console.error("getMondayOfWeek error:", e);
                return ""; // o "Error de fecha"
            }
        }

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
