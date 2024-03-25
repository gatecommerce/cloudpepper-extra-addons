/** @odoo-module */
import { NfOrderListScreen } from "@nf_pos_order_list/screens/order_list/order_list";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";

patch(NfOrderListScreen.prototype, {
    async nfPayOrder(order) {
        let product = await this.pos.db.get_product_by_id(this.pos.config.nf_partial_payment_product[0])
        let amount = 0 
        order.get_paymentlines().forEach((line) => {
            if (!line.payment_method.split_transactions){
                amount += line.amount
            }
        })
        await order.add_product(product, {
            quantity: -1,
            price: amount,
            lst_price: amount,
            extras: { price_type: "automatic" },
        })
        
        if ( order.get_paymentlines() ){
            [...order.get_paymentlines()].map(async (line) => {
                await order.remove_paymentline(line)
            })
        }
        order.set_is_partial_payment(true)
        order['get_partial_payment'] = true
        await this.pos.set_order(order);
        this.env.services.pos.showScreen("PaymentScreen");
    },
    getAmountPaid(order){
        let amounts = order.get_paymentlines().map(( x )=> {
            if (!x.payment_method.split_transactions){
                return x.amount
            }else{
                return 0
            }
        })
        return this.env.utils.formatCurrency(amounts.reduce((b, a) => a + b, 0))
    },
    _computeSyncedOrdersDomain() {
        const { filter } = this._state.ui;
        const domain =  super._computeSyncedOrdersDomain()
        if (filter == "PARTIAL") {
            domain.push(["state", "=", "partial_paid"]);
        }
        return domain
    },
    _getOrderStates() {
        var states = super._getOrderStates()
        states.set("PARTIAL", {
            text: _t("Partial Paid"),
        });
        return states
    }
})
