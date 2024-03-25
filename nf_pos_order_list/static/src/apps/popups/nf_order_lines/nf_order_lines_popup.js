/** @odoo-module */

import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { usePos } from "@point_of_sale/app/store/pos_hook";

/**
 * Props:
 *  {
 *      info: {object of data}
 *  }
 */
export class nfPosOrderLinesPopup extends AbstractAwaitablePopup {
    static template = "nf_pos_order_list.nfPosOrderLinesPopup";
   
    setup() {
        super.setup();
        this.pos = usePos();
    }
}
