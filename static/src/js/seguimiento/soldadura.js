/** @odoo-module **/
import { Component, onWillStart } from "@odoo/owl";

export class Soldadura extends Component{
    setup(){
        this.state = {
            soldadura: [],
        }

        onWillStart(async () => {
            await this.soldaduraData();
        });
    }

    async soldaduraData(){
        const response = await fetch("/soldadura_ordenes");
        const data = await response.json();
        console.log(data);
        this.state.soldadura = data;
    };

}

Soldadura.template = "dtm_procesos.soldadura_template"

