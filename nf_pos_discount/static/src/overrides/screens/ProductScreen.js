/** @odoo-module */

import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";
import { parseFloat } from "@web/views/fields/parsers";
import { NumberPopup } from "@point_of_sale/app/utils/input_popups/number_popup";
import { _t } from "@web/core/l10n/translation";

patch(ProductScreen.prototype, {
    async onNumpadClick(buttonValue) {
        super.onNumpadClick(...arguments);
        const mode = buttonValue
        if (
            mode === "discount" &&
            this.pos.config.nf_enbale_price_discount
        ) {
            let order = this.pos.get_order();
            if (order.get_selected_orderline()) {
                const { confirmed, payload } = await this.popup.add(NumberPopup, {
                        title: _t("Discount"),
                        startingValue: 1,
                        isInputSelected: true,
                        is_custom_discount: true,
                    }
                );
                if (confirmed) {
                    if (payload && payload.discount_type == "amount") {
                        let line =order.get_selected_orderline()
                        if(line.get_discount() > 0){
                            const Totalprice = order.get_total_with_tax();
                            const discountamount = payload.amount;
                            const newTotalprice =  await order.get_total_with_tax();
                            await line.set_discount(0);
                            let discounted_Amount = newTotalprice - Totalprice
                            let set_discount_amount = discounted_Amount + discountamount
                            var lineDiscountPercentage = (set_discount_amount / newTotalprice) * 100;
                            
                            await line.set_discount(lineDiscountPercentage)
                        }else{
                       
                            const Totalprice = order
                                .get_selected_orderline()
                                .get_display_price();
                            const discountamount = payload.amount;
                            var percentage = (discountamount / Totalprice) * 100;
                            percentage = percentage
                            let old_discount_amount = order.get_nf_global_discount()
                            order.set_nf_global_discount(discountamount + old_discount_amount);
                            order.get_selected_orderline().set_discount(percentage);
                        }
                    } else {
                        await order.get_selected_orderline().set_discount(payload);
                    }
                }
            }
        }
    },
});