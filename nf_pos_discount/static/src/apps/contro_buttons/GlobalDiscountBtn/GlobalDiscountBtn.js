/** @odoo-module */

import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { Component } from "@odoo/owl";
import { NumberPopup } from "@point_of_sale/app/utils/input_popups/number_popup";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import {
    formatFloat,
    roundDecimals as round_di,
    roundPrecision as round_pr,
    floatIsZero,
} from "@web/core/utils/numbers";

export class NfGlobalDiscountBtn extends Component {
    static template = "nf_pos_discount.NfGlobalDiscountBtn";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
    }
    async onClick() {
        var order = this.pos.get_order();
        if (order) {
            const { confirmed, payload } = await this.popup.add(NumberPopup, {
                title: _t("Discount"),
                startingValue: 1,
                isInputSelected: true,
                is_custom_discount: true,
            });
            if (confirmed) {
                if (payload && payload.discount_type == "amount") {
                    order.set_nf_global_discount(0.00);
                    const Totalprice = order.get_total_with_tax();
                    const discountamount = payload.amount;
                    order.set_nf_global_discount(discountamount);
                    var percentage = (discountamount / Totalprice) * 100;
                    [...order.get_orderlines()].map(async (line) => {

                        if(line.get_discount() > 0){
                            await line.set_discount(0);
                            const newTotalprice =  await order.get_total_with_tax();
                            let discounted_Amount = newTotalprice - Totalprice
                            let set_discount_amount = discounted_Amount + discountamount
                            var lineDiscountPercentage = (set_discount_amount / newTotalprice) * 100;
                            
                            await line.set_discount(lineDiscountPercentage)
                        }else{
                            await line.set_discount(percentage)
                        }
                        // await line.set_discount(percentage)
                    })
                } else {
                    const val = Math.round(
                        Math.max(0, Math.min(100, parseFloat(payload)))
                        );
                        const Totalprice = order.get_total_with_tax();
                        var percentage = (Totalprice * val) / 100;
                        var lineDiscountPercentage = (percentage / Totalprice) * 100;
                        
                        if( order.get_orderlines()[0].get_discount() ){
                            var before_discount = await order.get_total_discount() + Totalprice;
                        
                            [...order.get_orderlines()].map(async (line) => {
                                await line.set_discount(0);
                            })
                            const before_discount_total = order.get_total_with_tax();
                            var after_discount_amount = (Totalprice * val) / 100;
                            var total_discount_amount = after_discount_amount
                        
                            const newTotalprice =  await order.get_total_with_tax();
                            let discounted_Amount = newTotalprice - Totalprice
                            let set_discount_amount = discounted_Amount + total_discount_amount
                            var lineDiscountPercentage = (set_discount_amount / newTotalprice) * 100;
                            
                        }
                        [...order.get_orderlines()].map(async (line) => {
                            if(line.get_discount() > 0){
                                line.set_discount(lineDiscountPercentage)
                            }else{
                                await line.set_discount(lineDiscountPercentage)
                            }
                        })
                    order.set_nf_global_discount(percentage);
                }
            }
        } else {
            this.popup.add(ErrorPopup, {
                title: _t("Discount!"),
                body: _t(
                    "Please Add Product in Cart !"
                ),
            });
        }
    }
}

ProductScreen.addControlButton({
    component: NfGlobalDiscountBtn,
    condition: function () {
        return this.pos.config.nf_enbale_price_discount;
    },
});

