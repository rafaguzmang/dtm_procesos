/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

//console.log("indicacor de Procesos");

export class Indicador extends Component {
    setup() {
    super.setup();
    const http = useService("http");
    this.canvasRef = useRef("grafico");
    this.state = useState({
      items: []
    });

      onMounted(async () => {
        // Espera un poco para asegurar que los scripts externos hayan cargado
        await new Promise(resolve => setTimeout(resolve, 100));

        // Asegura que el plugin esté disponible y lo registra
        if (window['chartjs-plugin-annotation']) {
            Chart.register(window['chartjs-plugin-annotation']);
        }

        // Autenticación
        const body = {
          jsonrpc: "2.0",
          method: "call",
          params: {
            service: "common",
            method: "authenticate",
            args: ["backup", "rafaguzmang@hotmail.com", "admin", {}], // Contraseña
          },
          id: Math.floor(Math.random() * 1000),
        };

        try {
          const response = await fetch("/jsonrpc", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
            credentials: "include", // Muy importante para mantener la sesión
          });
          const data = await response.json();
//          console.log("🔐 Data:", data.result);
        } catch (error) {
          console.error("❌ Error al obtener datos:", error);
        }

        // Obtener datos para la tabla
        const readBody = {
          jsonrpc: "2.0",
          method: "call",
          params: {
            model: "dtm.procesos.indicadores",
            method: "search_read",
            args: [
              [["id", "!=", 0]], // Dominio (puedes ajustar)
              [
                "id",
                "no_month",
                "mes",
                "ordenes",
                "en_tiempo",
                "tarde",
                "porcentaje",
              ], // Campos a leer
            ],
            kwargs: {
              limit: 12,
            },
          },
          id: Math.floor(Math.random() * 1000),
        };

        try {
            const readResponse = await fetch("/web/dataset/call_kw", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(readBody),
                credentials: "include",
            });

            const readData = await readResponse.json();
//            console.log("📦 Datos obtenidos:", readData.result);

              // Asigna los datos al estado
            this.state.items = readData.result;

            const canvas = this.canvasRef.el;
            const ctx = canvas.getContext("2d");
//            Se arreglan los valores para mostrarlos en la tabla
            this.state.items = this.state.items.map(row =>(
            {
                ...row,
                porcentaje:(row.porcentaje).toFixed(2)

            }));
//            console.log(this.state.items);
            const labels = this.state.items.map(item => item.mes);
            const data = this.state.items.map(item => item.porcentaje);
//            console.log(labels);
//            console.log(data);
//            Grafica
            new Chart(ctx, {
                type: "bar", // o "line", "pie", etc.
                data: {
                      labels: labels,
                      datasets: [{
                          label: "Cotizaciones por mes",
                          data: data,
                          backgroundColor: "rgba(75, 192, 192, 0.2)",
                          borderColor: "rgba(75, 192, 192, 1)",
                          borderWidth: 1
                      }]
                  },
                options: {
                    responsive: true,
                    plugins: {
                        annotation: {
                            annotations: {
                                line1: {
                                    type: 'line',
                                    yMin: 80,  // 60% en escala de 0 a 100
                                    yMax: 80,  // 60% en escala de 0 a 100
                                    borderColor: 'rgba(0,255,0,0.4)',
                                    borderWidth: 2,
                                    label: {
                                        content: '',
                                        enabled: true,
                                        position: 'start'
                                    }
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100  // Escala de 0 a 100
                        }
                    }
                }
              });

          } catch (error) {
            console.error("❌ Error al leer datos:", error);
          }
    });


  }
}

Indicador.template = "dtm_procesos.indicador";

registry.category("actions").add('dtm_procesos.indicador', Indicador);




