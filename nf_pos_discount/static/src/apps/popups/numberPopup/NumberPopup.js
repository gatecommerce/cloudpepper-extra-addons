/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { parseFloat } from "@web/views/fields/parsers";
import { NumberPopup } from "@point_of_sale/app/utils/input_popups/number_popup";
import { _t } from "@web/core/l10n/translation";

patch(NumberPopup.prototype, {
    setup() {
        super.setup();
        this.discount_type = "percentage";
    },
    setType() {
        this.discount_type = "amount";
    },
    getPayload() {
        if (this.discount_type == "amount") {
            return {
                discount_type: this.discount_type,
                amount: parseFloat(this.numberBuffer.get()),
            };
        } else {
            return parseFloat(this.numberBuffer.get())
        }
    },
});
