/** @odoo-module */
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { ConfirmPopup } from "@point_of_sale/app/utils/confirm_popup/confirm_popup";
import { _t } from "@web/core/l10n/translation";
import { Order } from "@point_of_sale/app/store/models";

patch(PaymentScreen.prototype, {
    async toggleIsPartialPayment() {
        // Click Partial Payment
        var self = this;
        this.currentOrder.set_is_partial_payment(
            !this.currentOrder.is_partial_payment()
        );
            [...this.currentOrder.get_paymentlines()].map(async (line) => {
                if (line.payment_method.split_transactions && !self.currentOrder.get_partial_payment) {
                    await self.currentOrder.remove_paymentline(line);
                }
            });
        this.render();
    },
    async validateOrder(isForceValidate) {
        if (this.currentOrder.is_partial_payment() || this.currentOrder.get_partial_payment) {
            let payment_method = this.pos.payment_methods.filter(
                (pay) => pay.split_transactions
            );
            if ( this.currentOrder.get_partial_payment ){
                let old_line_amount = this.currentOrder.selected_paymentline.amount
                const newPaymentline = await this.currentOrder.add_paymentline(payment_method[0]);
                newPaymentline.set_amount( -old_line_amount );
            } else{
                this.currentOrder.add_paymentline(payment_method[0]);
            }
        }
        await super.validateOrder(...arguments)  
    },
    async _finalizeValidation() {
        await super._finalizeValidation()
        var self = this;
        if (this.currentOrder.get_partial_payment){
            this.currentOrder.finalized = false;
            let order_id = this.currentOrder.export_as_JSON().server_id
            if (order_id){
                delete self.pos.ORDERLIST_SCREEN_STATE.syncedOrders.cache[order_id]
            }
        }
    },
    async _isOrderValid(isForceValidate) {
        if (
            this.currentOrder.is_partial_payment() &&
            !this.currentOrder.get_partner()
        ) {
            const { confirmed } = await this.popup.add(ConfirmPopup, {
                title: _t("Please select the Customer"),
                body: _t(
                    "You need to select the customer before you can take Partial Payment."
                ),
            });
            if (confirmed) {
                this.selectPartner();
            }
            return false;
        }else{
            return super._isOrderValid(...arguments);
        }
        return true
    },
});
