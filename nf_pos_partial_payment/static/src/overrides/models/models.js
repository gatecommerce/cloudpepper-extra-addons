
/** @odoo-module */

import { Order, Orderline, Payment } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        if (this.pos.config.nf_pos_enable_order_list &&this.pos.config._nf_pos_enable_partial_payment) {
            this.nf_is_partial_payment = false;
            this.get_partial_payment = false
        }
    },
    //@override
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        if (this.pos.config.nf_pos_enable_order_list && this.pos.config._nf_pos_enable_partial_payment) {
            this.nf_is_partial_payment = json.nf_is_partial_payment;
        }
    },
    //@override
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        if (this.pos.config.nf_pos_enable_order_list && this.pos.config._nf_pos_enable_partial_payment) {
            json.nf_is_partial_payment = this.nf_is_partial_payment;
        }
        if( this.is_partial_payment() ){
            json['state'] = "draft"
        }
        return json;
    },
    is_paid() {
        var res = super.is_paid();
        if( this.pos.config.nf_pos_enable_order_list && this.pos.config._nf_pos_enable_partial_payment && this.nf_is_partial_payment ){
            res = this.is_partial_payment();
        }
        return res
    },
    set_is_partial_payment(nf_partial_payment) {
        this.assert_editable();
        this.nf_is_partial_payment = nf_partial_payment;
    },
    is_partial_payment() {
        return this.nf_is_partial_payment
    }
})

