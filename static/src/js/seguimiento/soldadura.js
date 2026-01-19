/** @odoo-module **/
import { Component, onWillStart, onMounted, onWillUnmount, useState } from "@odoo/owl";

export class Soldadura extends Component{
    setup(){
        this.state = useState({
            soldadura: [],
        });
        let interval = null;

        onWillStart(async () => {
            await this.soldaduraData();
        });

        onMounted(()=>{
            interval = setInterval(() => {
                this.soldaduraData();
            },5000)
        })

        onWillUnmount(() => {
            clearInterval(interval);
        });

    }

    async soldaduraData(){
        const response = await fetch("/soldadura_ordenes");
        const data = await response.json();
        console.log("Funciona")
        this.state.soldadura = data;
    };

}

Soldadura.template = "dtm_procesos.soldadura_template"

