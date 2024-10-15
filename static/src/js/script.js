odoo.define('dtm_procesos.script', function (require) {
    "use strict";

    $(document).ready(function () {
        console.log("dtm_procesos.script")
        var tabla = $('.o_kanban_renderer');
        console.log("tabla: " + tabla)

    });
////    var domReady = require('web.dom_ready');
////
////    domReady(function() {
////        alert("funciona")
////        var tabla = document.querySelector('.o_kanban_renderer');
//
////        console.log("El DOM está listo, ahora puedes interactuar con él.");
////
////        // Verifica si el elemento existe
////        var renderer = document.querySelector('.o_kanban_renderer');
////        console.log("Elemento .o_kanban_renderer:", renderer);
////
////        if (renderer) {
////            // Manipula el DOM aquí
////            console.log("El elemento fue encontrado.");
////        } else {
////            console.log("El elemento .o_kanban_renderer no se encontró en el DOM.");
////        }
////        console.log("Tabla: " + tabla)
////        var colums = tabla[0].children.length;
////        for(let i=0;i<colums;i++){
////                var text = tabla[0].children[i].children[0].children[0].children[0].innerText;
////                if(text == 'Pendiente a aprobación'){
////                    tabla[0].children[i].style = "order:1";
////                }else if(text == 'Corte'){
////                    tabla[0].children[i].style = "order:2";
////                }else if(text == 'Revisión FAI'){
////                    tabla[0].children[i].style = "order:3";
////                }else if(text == 'Doblado'){
////                    tabla[0].children[i].style = "order:4";
////                }else if(text == 'Soldadura'){
////                    tabla[0].children[i].style = "order:5";
////                }else if(text == 'Lavado'){
////                    tabla[0].children[i].style = "order:6";
////                }else if(text == 'Pintura'){
////                    tabla[0].children[i].style = "order:7";
////                }else if(text == 'Ensamble'){
////                    tabla[0].children[i].style = "order:8";
////                }else if(text == 'Servicio Externo'){
////                    tabla[0].children[i].style = "order:9";
////                }else if(text == 'Calidad'){
////                    tabla[0].children[i].style = "order:10";
////                }else if(text == 'Instalación'){
////                    tabla[0].children[i].style = "order:11";
////                }else if(text == 'Terminado'){
////                    tabla[0].children[i].style = "order:12";
////                }
////        }
////        var columna = tabla[0].children[0];
////        column = columna.children.length-1;
////        var date = '';
////        var date2 = '';
////        for(let i=1;i<column;i++){
////            if (columna.children[i].querySelectorAll('ul')[0].children[4].children && columna.children[i + 1].querySelectorAll('ul')[0].children[4].children){
////                date = columna.children[i].querySelectorAll('ul')[0].children[4].children[0].innerText;
////                date2 = columna.children[i+1].querySelectorAll('ul')[0].children[4].children[0].innerText;
////                console.log(i + ": "+date + " " + date2);
////            }
////        }
//
//    });
//
//
});

