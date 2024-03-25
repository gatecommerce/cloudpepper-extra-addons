/** @odoo-module */

import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { useState, useRef, onMounted } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ConfirmPopup } from "@point_of_sale/app/utils/confirm_popup/confirm_popup";

export class MultiChoicePopup extends AbstractAwaitablePopup {
    static template = "bi_pos_order_restore.MultiChoicePopup";

    static defaultProps = {
        confirmText: 'Select',
        cancelText: 'Cancel',
        body: '',
    };

    setup() {
        super.setup();
        this.popup = useService("popup");
        this.pos = usePos();
    }
    async delete_data() {
        const { confirmed } = await this.popup.add(ConfirmPopup, {
            title: _t('Confirmation !!'),
            body: _t(
                'This will remove the locally stored unsaved orders.'
            ),
        });
        if (confirmed) {
            var unsync_orders = this.pos.get_order().get_unsend_order();
            if(unsync_orders){
                for(var order of unsync_orders){
                    this.pos.db.remove_order(order.id);
                }
                this.pos.get_order().set_unsend_order(false);
                $('.cloud_button').hide()
                this.cancel()
                this.pos.set_synch('disconnected', this.pos.db.get_orders().length);
            }
        } else {
            this.cancel()
        }
    }

    async download_data() {
            var link;
            var unsync_orders = this.pos.get_order().get_unsend_order();
            var offline_data_list = []
            if (unsync_orders.length > 0){
                for (let i = 0; i < unsync_orders.length; i++) {
                    offline_data_list.push(unsync_orders[i])
                }
            }
            var link;
            var json = 'data:text/json;charset=utf-8,' + JSON.stringify(offline_data_list);
            var filename = 'restore_order_data.json';
            var data = encodeURI(json);
            link = document.createElement('a');
            link.setAttribute('href', data);
            link.setAttribute('download', filename);
            link.click();
            const { confirmed } = await this.popup.add(ConfirmPopup, {
                title: _t('Confirmation !!'),
                body: _t('Remove locally stored unsaved orders ?'),
            });
            if (confirmed) {
                if(unsync_orders){
                    for(var order of unsync_orders){
                        this.pos.db.remove_order(order.id);
                    }
                    this.pos.get_order().set_unsend_order(false);
                    $('.cloud_button').hide()
                    this.cancel()
                    this.pos.set_synch('disconnected', this.pos.db.get_orders().length);
                }
            } else{
                this.cancel()
            }
        }

        cancel() {
            this.props.close({ confirmed: false, payload: null });
        }
    }


