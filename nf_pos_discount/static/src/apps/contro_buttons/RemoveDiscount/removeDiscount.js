/** @odoo-module */

import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { Component } from "@odoo/owl";
import { NumberPopup } from "@point_of_sale/app/utils/input_popups/number_popup";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";


export class NfGlobalDiscountBtn extends Component {
    static template = "nf_pos_discount.NfremoveDiscountBtn";

    setup() {
        this.pos = usePos();
    }
    async onClick() {
        var order = this.pos.get_order()
        if (order){
            [...order.get_orderlines()].map(async (line) => {
                await line.set_discount(0)
            })
            order.set_nf_global_discount(0);
        }
    }
}

ProductScreen.addControlButton({
    component: NfGlobalDiscountBtn,
    condition: function () {
        return this.pos.config.nf_enbale_price_discount;
    },
});

