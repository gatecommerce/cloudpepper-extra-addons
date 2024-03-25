/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {

    set_synch(status, pending) {
        if (["connected", "connecting", "error", "disconnected"].indexOf(status) === -1) {
            console.error(status, " is not a known connection state.");
        } else if (status === "connected") {
            this.showOfflineWarning = true;
        }

        pending =
            pending || this.db.get_orders().length + this.db.get_ids_to_remove_from_server().length;
        this.synch = { status, pending };
    }
});
