/** @odoo-module **/
import { Component, onWillStart, onMounted, onWillUnmount, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class Soldadura extends Component{
    setup(){
        this.state = useState({
            soldadura: [],
        });
        this.busService = useService("bus_service");
        this.onBusNotification = this.onBusNotification.bind(this);        

        onWillStart(async () => {
            await this.soldaduraData();

            this.busService.addChannel("canal_soldadura");
            this.busService.addEventListener('notification',this.onBusNotification);
        });

        onMounted(()=>{           
            this.soldaduraData();
        })

        onWillUnmount(() => {
            clearInterval(interval);
        });

    }

    onBusNotification(notifications) {
        console.log("Paquete recibido del bus:", notifications);
        console.log("notifications.detail",notifications.detail[0].payload.mensaje);
        this.soldaduraData();
    }

    async soldaduraData(){
        const response = await fetch("/soldadura_ordenes");
        const data = await response.json();
        this.state.soldadura = data;
    };

}

Soldadura.template = "dtm_procesos.soldadura_template"

