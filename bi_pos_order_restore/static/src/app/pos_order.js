/** @odoo-module */

import { Order, Orderline, Payment } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.unsend_order = this.pos.db.get_orders() || false;
    },
    init_from_JSON(json){
        super.init_from_JSON(...arguments);
        this.unsend_order = json.unsend_order;
    },
    set_unsend_order(order){
        this.unsend_order = order;
    },
    get_unsend_order() {
        return this.unsend_order;
    },
});