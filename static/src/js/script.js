odoo.define('dtm_procesos.script', function (require) {
    "use strict";

    var KanbanRecord = require('web.KanbanRecord');

    KanbanRecord.include({
        start: function () {
            this._super.apply(this, arguments);
            // Tu código JavaScript aquí
            console.log("¡Hola desde script.js!");
        },
    });
});
