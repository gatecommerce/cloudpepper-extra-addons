
/** @odoo-module */

import { Navbar } from "@point_of_sale/app/navbar/navbar";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import {ErrorPopup} from "@point_of_sale/app/errors/popups/error_popup";
import { useService } from "@web/core/utils/hooks";
import { MultiChoicePopup } from "@bi_pos_order_restore/app/MultiChoicePopup";
import { _t } from "@web/core/l10n/translation";

patch(Navbar.prototype, {

	setup() {
        super.setup();
        this.pos = usePos();
        this.popup = useService("popup");
    },
    async onClick() {
            const { confirmed } = await this.popup.add(MultiChoicePopup, {
                title:_t("Choose Your Operation")
            });
    }

});

