    /** @odoo-module **/
import { Component, onWillStart } from "@odoo/owl";


export class DialogMaterialesLiberar extends Component{
    static props = ["cerrar", "orden", "version"];
    setup(){
        this.state = {
            materiales: [],
        };

        onWillStart(async()=>{
            await this.cargarMateriales();
        });
    }

     async cargarMateriales(){
        console.log(this.props.orden);
        const response = await fetch("/liberar_materiales", {
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
        console.log('resultdata',this.state.materiales);
    }
}

DialogMaterialesLiberar.template = "dtm_procesos.dialog_material_liberar";
