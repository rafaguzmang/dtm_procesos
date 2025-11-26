/** @odoo-module **/
import { Component, onWillStart, useState, onMounted,onWillUnmount } from "@odoo/owl";

export class CorteLaser extends Component{
    setup(){
        this.state = useState({
            mitsubishi: null,
            jfy: null,
            cortes:[],
            data:[],
            // Tiempos diarios
            tiempo_mitsubishi:0,
            tiempo_jfy:0,
            tiempo_estimado_mitsubishi:0,
            tiempo_estimado_jfy:0,
            // Porcentaje de corte
            porcentaje_corte:0,
            porcentaje_mitsubishi:0,
            porcentaje_jfy:0,
        });
        let interval = null;
        onWillStart(async () => {
            await this.maquinasData();
            await this.cortesLaser();
            await this.tiempoDiario();
        });

        onMounted(() => {
            interval = setInterval(() => {
                this.maquinasData();
                this.cortesLaser();
                this.tiempoDiario();
            }, 5000);
        });

        onWillUnmount(() => {
            clearInterval(interval);
        });


    }
    async cortesLaser(){
        const response = await fetch("/corte_diario");
        const data = await response.json();
        // console.log('data',data);
        let id = 0;
        this.state.cortes = data.map(item => ({id: id++, ...item}));
        const mitsubishidata = this.state.cortes.filter(item => item.cortadora === "MITSUBISHI");
        const jfyData = this.state.cortes.filter(item => item.cortadora === "BFC6025");
        this.state.tiempo_estimado_mitsubishi = Number(mitsubishidata.reduce((total, corte) => total + (corte.tiempo_teorico || 0), 0)).toFixed(2);
        this.state.tiempo_estimado_jfy = Number(jfyData.reduce((total, corte) => total + (corte.tiempo_teorico || 0), 0)).toFixed(2);
        this.state.tiempo_real = Number(this.state.cortes.reduce((total, corte) => total + (corte.tiempo_real || 0), 0)).toFixed(2);
        const avance = Number(this.state.cortes.reduce((total,corte)=> total + (corte.porcentaje||0),0)).toFixed(2);
//        console.log(avance);
        this.state.porcentaje_corte = Number((avance * 100)/(id * 100)).toFixed(2);
        console.log('this.state.porcentaje_corte',this.state.porcentaje_corte);
    }

    // Obtener tiempos diarios de uso de las maquinas
    async tiempoDiario(){
        const response = await fetch("/corte_tiempos");
        const data = await response.json();
        console.log(data);
        this.state.tiempo_mitsubishi = data.mitsubishi;
        this.state.tiempo_jfy = data.jfy;
        this.state.porcentaje_mitsubishi =Math.round(data.mitsubishi*100/540,0);
        this.state.porcentaje_jfy = Math.round(data.jfy*100/540,0);
    }

    async maquinasData(){
        const response = await fetch("/maquinas_corte");
        const data = await response.json();
//        console.log(data);
        let id = 0;
        const newData = data.map(item => ({id: id++, ...item}));
        this.state.data = newData;
        // console.log(this.state.data);
        const mitsubishidata = newData.filter(item => item.cortadora === "MITSUBISHI");
        this.state.mitsubishi = mitsubishidata[0]?.archivo||null;
        const jfyData = newData.filter(item => item.cortadora === "BFC6025");
        this.state.jfy = jfyData[0]?.archivo||null;
//        console.log('mitsubishi',this.state.mitsubishi);
//        console.log('jfy',this.state.jfy);
    }
}

CorteLaser.template = "dtm_procesos.corte_laser_template";
