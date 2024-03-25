/** @odoo-module */

import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { Component } from "@odoo/owl";

export class NfOrderListButton extends Component {
    static template = "nf_pos_order_list.NfOrderListButton";

    setup() {
        this.pos = usePos();
    }
    click() {
        const order = this.pos.get_order();
        const partner = order.get_partner();
        const searchDetails = partner ? { fieldName: "PARTNER", searchTerm: partner.name } : {};
        this.pos.showScreen("NfOrderListScreen", {
            ui: { filter: "SYNCED", searchDetails },
            destinationOrder: order,
        });
    }
}

ProductScreen.addControlButton({
    component: NfOrderListButton,
    condition: function () {
        return this.pos.config.nf_pos_enable_order_list;
    },
});
