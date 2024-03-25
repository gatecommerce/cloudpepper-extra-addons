
/** @odoo-module */

import { Order, Orderline } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";


patch(Order.prototype, {
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.nf_global_discoount = this.get_nf_global_discount() || 0.00
    },
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        
        json.employee_id = this.cashier ? this.cashier.id : false;
        
        return json;
    },
    get_nf_global_discount(){
        return this.nf_global_discoount
    },
    set_nf_global_discount(discount){
        this.nf_global_discoount = discount
    }
})

patch(Orderline.prototype,{
    getDisplayData() {
        let res = super.getDisplayData()
        if(res.discount !== '0'){
          let int_discount =  parseFloat(res.discount).toFixed(2)
          res["discount"] = int_discount
        }
        return res
      },
})
