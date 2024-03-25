# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    "name": "All in One Views",
    "author": "Softhealer Technologies",
    "license": "OPL-1",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "version": "0.0.2",
    "category": "Extra Tools",
    "summary": "Show Incoming Order Lines Display Outgoing Order Lines Display Delivery Order Lines Show Shipment Line Views Show Purchase Order Lines Show Request For Quotation Lines Show Quotation Lines Show credit note lines Show debit note lines Show picking order lines Display credit note order lines Display debit note order lines Display picking order lines Display Sale Order Lines All In One Line Views Odoo Sale Order Line Views Sales Order Line Views Sale Line View Sales Line View SO Line Views Quotations Line Views Purchase Order Line Views Purchase Line View PO Line Views Picking Order Line Views Invoice Line View All Lines View Kanban View Pivot View Graph View Calendar View Search View Form View All in One lines View So kanban view Sale order kanban view Sale order form view So form view Sale order search view So search view Sale order pivot view So pivot view Sale order list view So list view Sale order graph view So graph view Purchase order list view Purchase order kanban view Purchase order form view Purchase order pivot view Purchase order search view Purchase order graph view PO list view PO kanban view PO form view PO pivot view PO search view PO graph view Invoice order list view Invoice order kanban view Invoice order form view Invoice order pivot view Invoice order search view Invoice order graph view Bill orders list view Bill order kanban view Bill order form view Bill order pivot view Bill order search view Bill order graph view Credit note order list view Credit note order kanban view Credit note order form view Credit note order pivot view Credit note order search view Credit note order graph view Debit note order list view Debit note order kanban view Debit note order form view Debit note order pivot view Debit note order search view Debit note order graph view RFQ order list view RFQ order kanban view RFQ order form view RFQ order pivot view RFQ order search view RFQ order graph view Picking order list view Picking order kanban view Picking order form view Picking order pivot view Picking order search view Picking order graph view",
    "description": """
This module useful to show sale order/quotation purchase order/request for quotation incoming order/outgoing order/bill/invoice/credit note/debit note refund lines products and other information related to it using the filter & group by option. You can easily add custom filters/groups of sale order/quotation/purchase order/request for quotation incoming order/outgoing order/bill/invoice/credit note/debit note refund order lines. Easy to work with sale order/quotation purchase order/request for quotation/incoming order/outgoing order bill/invoice/credit note/debit note/refund lines directly using the list view, form view, kanban view, search view, pivot view, graph view, calendar view. All In One Line Views Odoo Show Incoming Order Lines, Display Outgoing Order Lines Module, Display  Delivery Order Lines, Show Shipment Line Views, Show Incoming Order Lines, Display Outgoing Order Lines, Show Purchase Order  Lines, Show Request For Quotation  Lines, Show Quotation Lines, Display Sale Order Lines Odoo Show Incoming Order Lines, Display Outgoing Order Lines Module, Display  Delivery Order Lines, Show Shipment Line Views, Show Incoming Order Lines App, Display Outgoing Order Lines, Show Purchase Order  Lines, Show Request For Quotation  Lines, Show Quotation Lines, Display Sale Order Lines Odoo
""",
    "depends": ["sale_management", "account", "purchase", "stock"],
    "data": [
        "views/account_move_line_views.xml",
        "views/purchase_order_line_views.xml",
        "views/sale_order_line_views.xml",
        "views/stock_move_views.xml",
    ],
    "images": [
        "static/description/background.png",
    ],
    "live_test_url": "https://youtu.be/LjAyw4WuXqw",
    "auto_install": False,
    "installable": True,
    "application": True,
    "price": 40,
    "currency": "EUR",
}
