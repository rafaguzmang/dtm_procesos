/** @odoo-module **/
import { Component, onWillStart, useState, onMounted,onWillUnmount } from "@odoo/owl";

export class CorteLaser extends Component{
    setup(){
        this.state = useState({
            mitsubishi: [],
            jfy: [],
        });
        let interval = null;
        onWillStart(async () => {
            await this.mitsubishiData();
        });

        onMounted(() => {
            interval = setInterval(() => {
                this.mitsubishiData();
            }, 5000);
        });

        onWillUnmount(() => {
            clearInterval(interval);
        });


    }
    async mitsubishiData(){
        const response = await fetch("/maquinas_corte");        
        const data = await response.json();
        console.log(data);
        let id = 0;
        const newData = data.map(item => ({id: id++, ...item}));
        this.state.mitsubishi = newData.filter(item => item.cortadora === "MITSUBISHI");
        this.state.jfy = newData.filter(item => item.cortadora === "BFC6025");
        console.log(this.state.mitsubishi);
        console.log(this.state.jfy);
    }
}

CorteLaser.template = "dtm_procesos.corte_laser_template";