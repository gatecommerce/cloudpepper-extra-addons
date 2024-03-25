/** @odoo-module */

import { Order } from "@point_of_sale/app/store/models";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import {
    deserializeDateTime,
    deserializeDate,
    formatDateTime,
} from "@web/core/l10n/dates";
import { _t } from "@web/core/l10n/translation";

import { SearchBar } from "@point_of_sale/app/screens/ticket_screen/search_bar/search_bar";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { nfPosOrderLinesPopup } from "@nf_pos_order_list/apps/popups/nf_order_lines/nf_order_lines_popup";
import { Component, onMounted, useState } from "@odoo/owl";

const { DateTime } = luxon;

export class NfOrderListScreen extends Component {
    static storeOnOrder = false;
    static template = "nf_pos_order_list.NfOrderListScreen";
    static components = {
        SearchBar,
    };
    static searchPlaceholder = _t("Search Orders...");
    setup() {
        this.pos = usePos();
        this.ui = useState(useService("ui"));
        this.popup = useService("popup");
        this.orm = useService("orm");
        this._state = this.pos.ORDERLIST_SCREEN_STATE;
        onMounted(this.onMounted);

        Object.assign(this._state.ui, this.props.ui || {});
    }
    onMounted() {
        setTimeout(() => {
            // Show updated list of synced orders when going back to the screen.
            this.onFilterSelected(this._state.ui.filter);
        });
    }
    async nfReorder(order){

        [...this.pos.get_order().get_orderlines()].map(async (line) => await this.pos.get_order().removeOrderline(line))

        var currentOrder = this.pos.get_order()

        if (order.get_partner()){
            await currentOrder.set_partner(order.get_partner())
        }

        if( order.get_orderlines() ){
            
        [...order.get_orderlines()].map(async (line) => await this.pos.get_order().add_orderline(line))

        }
        this.closeOrderListScreen()
    }
    async nfDisplayLines( order ){
        let orderLines = order.get_orderlines()
        this.popup.add(nfPosOrderLinesPopup, { lines: orderLines, 'total_tax': order.get_total_tax(), 'order_total': order.get_total_with_tax(), 'total_paid': order.get_total_paid() });
    }
    async onClickOrder(clickedOrder){
        this._state.ui.selectedOrder = clickedOrder;
    }
    async onFilterSelected(selectedFilter) {
        this._state.ui.filter = selectedFilter;
        await this._fetchSyncedOrders();
    }
    closeOrderListScreen() {
        this.pos.closeScreen();
    }
    getFilteredOrderList() {
        return this._state.syncedOrders.toShow;
    }
    getSelectedOrder() {
        if (this._state.ui.filter == "SYNCED" && this._state.ui.selectedOrder) {
            return this._state.syncedOrders.cache[
                this._state.ui.selectedOrder.backendId
            ];
        } else {
            return this._state.ui.selectedOrder;
        }
    }
    isHighlighted(order) {
        const selectedOrder = this.getSelectedOrder();

        return selectedOrder
            ? (order.backendId && order.backendId == selectedOrder.backendId) ||
                  order.uid === selectedOrder.uid
            : false;
    }
    nfGetSearchData() {
        return {
            searchFields: new Map(
                Object.entries(this._getSearchFields()).map(([key, val]) => [
                    key,
                    val.displayName,
                ])
            ),
            filter: { show: true, options: this._getFilterOptions() },
            defaultSearchDetails: this._state.ui.searchDetails,
            defaultFilter: this._state.ui.filter,
        };
    }
    _getFilterOptions() {
        const orderStates = this._getOrderStates();
        orderStates.set("SYNCED", { text: _t("All Orders") });
        return orderStates;
    }
    _getSearchFields() {
        const fields = {
            TRACKING_NUMBER: {
                repr: (order) => order.trackingNumber,
                displayName: _t("Order Number"),
                modelField: "tracking_number",
            },
            RECEIPT_NUMBER: {
                repr: (order) => order.name,
                displayName: _t("Receipt Number"),
                modelField: "pos_reference",
            },
            DATE: {
                repr: (order) =>
                    deserializeDate(order.date_order).toFormat(
                        "yyyy-MM-dd HH:mm a"
                    ),
                displayName: _t("Date"),
                modelField: "date_order",
            },
            PARTNER: {
                repr: (order) => order.get_partner_name(),
                displayName: _t("Customer"),
                modelField: "partner_id.complete_name",
            },
        };
        return fields;
    }
    getDate(order) {
        return formatDateTime(order.date_order);
    }
    getPartner(order) {
        return order.get_partner_name();
    }
    getCashier(order) {
        return order.cashier ? order.cashier.name : "";
    }
    getTotal(order) {
        return this.env.utils.formatCurrency(order.get_total_with_tax());
    }
    getStatus(order) {
        return _t(order.state);
    }
    nfPagination() {
        return this._getLastPage() > 1;
    }
    async onNextPage() {
        if (this._state.syncedOrders.currentPage < this._getLastPage()) {
            this._state.syncedOrders.currentPage += 1;
            await this._fetchSyncedOrders();
        }
    }
    async onPrevPage() {
        if (this._state.syncedOrders.currentPage > 1) {
            this._state.syncedOrders.currentPage -= 1;
            await this._fetchSyncedOrders();
        }
    }
    getPageNumber() {
        if (!this._state.syncedOrders.totalCount) {
            return `1/1`;
        } else {
            return `${this._state.syncedOrders.currentPage}/${this._getLastPage()}`;
        }
    }
    _getLastPage() {
        const totalCount = this._state.syncedOrders.totalCount;
        const nPerPage = this._state.syncedOrders.nPerPage;
        const remainder = totalCount % nPerPage;
        if (remainder == 0) {
            return totalCount / nPerPage;
        } else {
            return Math.ceil(totalCount / nPerPage);
        }
    }
    async onSearch(search) {
        Object.assign(this._state.ui.searchDetails, search);
        this._state.syncedOrders.currentPage = 1;
        await this._fetchSyncedOrders();
    }
    _computeSyncedOrdersDomain() {
        const { fieldName, searchTerm } = this._state.ui.searchDetails;
        const { filter } = this._state.ui;
        var domain = [];

        if (filter == "DONE") {
            domain.push(["state", "=", "done"]);
        } else if (filter == "INVOICED") {
            domain.push(["state", "=", "invoiced"]);
        } else if (filter == "PAID") {
            domain.push(["state", "=", "paid"]);
        }
        if (!searchTerm) {
            return domain;
        }
        const modelField = this._getSearchFields()[fieldName].modelField;
        if (modelField) {
            domain.push([modelField, "ilike", `%${searchTerm}%`])
            return domain
        } else {
            return domain;
        }
    }
    async _fetchSyncedOrders() {
        const domain = this._computeSyncedOrdersDomain();
        const limit = this._state.syncedOrders.nPerPage;
        const offset =
            (this._state.syncedOrders.currentPage - 1) *
            this._state.syncedOrders.nPerPage;
        const config_id = this.pos.config.id;
        const { ordersInfo, totalCount } = await this.orm.call(
            "pos.order",
            "search_paid_order_ids",
            [],
            { config_id, domain, limit, offset }
        );
        const idsNotInCache = await ordersInfo.filter(
            (orderinfo) => !(orderinfo[0] in this._state.syncedOrders.cache)
        );
        const cacheDate =
            this._state.syncedOrders.cacheDate || DateTime.fromMillis(0);
        const idsNotUpToDate = await ordersInfo.filter((orderInfo) => {
            return deserializeDateTime(orderInfo[1]) > cacheDate;
        });
        // contact ids
        const idsToLoad = idsNotInCache
            .concat(idsNotUpToDate)
            .map((info) => info[0]);
        if (idsToLoad.length > 0) {
            const fetchedOrders = await this.orm.call(
                "pos.order",
                "export_for_ui",
                [idsToLoad]
            );

            fetchedOrders.forEach((order) => {
                this._state.syncedOrders.cache[order.id] = new Order(
                    { env: this.env },
                    { pos: this.pos, json: order }
                );
            });
            this._state.syncedOrders.cacheDate = DateTime.local();
        }

        const ids = ordersInfo.map((info) => info[0]);
        this._state.syncedOrders.totalCount = totalCount;
        this._state.syncedOrders.toShow = ids.map(
            (id) => this._state.syncedOrders.cache[id]
        );
    }
    _getOrderStates() {
        const states = new Map();
        states.set("DONE", {
            text: _t("Done"),
        });
        states.set("PAID", {
            text: _t("Paid"),
        });
        states.set("INVOICED", {
            text: _t("Invoiced"),
        });
        return states;
    }
}
registry.category("pos_screens").add("NfOrderListScreen", NfOrderListScreen);
