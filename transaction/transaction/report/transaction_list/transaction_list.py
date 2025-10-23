# Copyright (c) 2025,   and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    VoucherType = filters.get("voucher_type")
    From = filters.get("from")
    To = filters.get("to")
    status = filters.get("status")
    customer = filters.get("customer")
    customer_grp = filters.get("customer_group")
    supplier = filters.get("supplier")
    supplier_grp = filters.get("supplier_group")
    data = []

    columns = [
        {
            "fieldname": "voucher_type",
            "label": "Voucher Type",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "voucher_no",
            "label": "Voucher No",
            "fieldtype": "Link",
            "width": 200,
            "options": VoucherType,
        },
        {"fieldname": "party", "label": "Party", "fieldtype": "Data", "width": 200},
        {
            "fieldname": "party_group",
            "label": "Party Group",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "posting_date",
            "label": "Posting Date",
            "fieldtype": "Data",
            "width": 200,
        },
        {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 200},
        {
            "fieldname": "total_amount",
            "label": "Total Amount",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "outstanding_amount",
            "label": "Outstanding Amount",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "actions",
            "label": "Actions",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "view_items",
            "label": "View Items",
            "fieldtype": "Data",
            "width": 200,
        },
    ]

    if VoucherType == "Sales Order":
        print(VoucherType)

        condition = {
            "docstatus": 1,
            "transaction_date": ["between", [From, To]],
        }
        if customer:
            condition["customer"] = customer

        if status:
            condition["status"] = status

        sales_order = frappe.db.get_all(
            "Sales Order",
            filters=condition,
            fields=[
                "name",
                "customer",
                "transaction_date",
                "status",
                "grand_total",
            ],
        )

        if customer_grp:
            for val in sales_order:
                party_grp = frappe.db.get_value(
                    "Customer", val["customer"], "customer_group"
                )
                if party_grp == customer_grp:
                    data.append(
                        {
                            "voucher_type": VoucherType,
                            "voucher_no": val["name"],
                            "party": val["customer"],
                            "party_group": party_grp,
                            "posting_date": val["transaction_date"],
                            "status": val["status"],
                            "total_amount": val["grand_total"],
                            # "outstanding_amount": val["outstanding_amount"],
                            "actions": "Actions",
                            "view_items": "View Items",
                        }
                    )

        else:

            for val in sales_order:
                party_grp = frappe.db.get_value(
                    "Customer", val["customer"], "customer_group"
                )

                data.append(
                    {
                        "voucher_type": VoucherType,
                        "voucher_no": val["name"],
                        "party": val["customer"],
                        "party_group": party_grp,
                        "posting_date": val["transaction_date"],
                        "status": val["status"],
                        "total_amount": val["grand_total"],
                        # "outstanding_amount": val["outstanding_amount"],
                        "actions": "Actions",
                        "view_items": "View Items",
                    }
                )

    elif VoucherType == "Sales Invoice":
        condition = {
            "docstatus": 1,
            "posting_date": ["between", [From, To]],
        }
        if customer:
            condition["customer"] = customer

        if status:
            condition["status"] = status

        sales_invoice = frappe.db.get_all(
            "Sales Invoice",
            filters=condition,
            fields=[
                "name",
                "customer",
                "posting_date",
                "status",
                "grand_total",
                "outstanding_amount",
            ],
        )

        if customer_grp:
            for val in sales_invoice:
                party_grp = frappe.db.get_value(
                    "Customer", val["customer"], "customer_group"
                )
                if party_grp == customer_grp:
                    data.append(
                        {
                            "voucher_type": "Sales Invoice",
                            "voucher_no": val["name"],
                            "party": val["customer"],
                            "party_group": party_grp,
                            "posting_date": val["posting_date"],
                            "status": val["status"],
                            "total_amount": val["grand_total"],
                            "outstanding_amount": val["outstanding_amount"],
                            "actions": "Actions",
                            "view_items": "View Items",
                        }
                    )

        else:

            for val in sales_invoice:
                party_grp = frappe.db.get_value(
                    "Customer", val["customer"], "customer_group"
                )

                data.append(
                    {
                        "voucher_type": "Sales Invoice",
                        "voucher_no": val["name"],
                        "party": val["customer"],
                        "party_group": party_grp,
                        "posting_date": val["posting_date"],
                        "status": val["status"],
                        "total_amount": val["grand_total"],
                        "outstanding_amount": val["outstanding_amount"],
                        "actions": "Actions",
                        "view_items": "View Items",
                    }
                )

    elif VoucherType == "Purchase Order":
        condition = {
            "docstatus": 1,
            "transaction_date": ["between", [From, To]],
            "status": ["not in", ["To Receive"]],
        }
        if supplier:
            condition["supplier"] = supplier

        if status:
            condition["status"] = status

        purchase_order = frappe.db.get_all(
            "Purchase Order",
            filters=condition,
            fields=[
                "name",
                "supplier",
                "transaction_date",
                "status",
                "grand_total",
            ],
        )

        if supplier_grp:
            for val in purchase_order:
                party_grp = frappe.db.get_value(
                    "Supplier", val["supplier"], "supplier_group"
                )
                if party_grp == supplier_grp:
                    data.append(
                        {
                            "voucher_type": "Purchase Order",
                            "voucher_no": val["name"],
                            "party": val["supplier"],
                            "party_group": party_grp,
                            "posting_date": val["transaction_date"],
                            "status": val["status"],
                            "total_amount": val["grand_total"],
                            # "outstanding_amount": val["outstanding_amount"],
                            "actions": "Actions",
                            "view_items": "View Items",
                        }
                    )

        else:

            for val in purchase_order:
                party_grp = frappe.db.get_value(
                    "Supplier", val["supplier"], "supplier_group"
                )

                data.append(
                    {
                        "voucher_type": "Purchase Order",
                        "voucher_no": val["name"],
                        "party": val["supplier"],
                        "party_group": party_grp,
                        "posting_date": val["transaction_date"],
                        "status": val["status"],
                        "total_amount": val["grand_total"],
                        # "outstanding_amount": val["outstanding_amount"],
                        "actions": "Actions",
                        "view_items": "View Items",
                    }
                )

    elif VoucherType == "Purchase Invoice":
        condition = {
            "docstatus": 1,
            "posting_date": ["between", [From, To]],
        }
        if supplier:
            condition["supplier"] = supplier

        if status:
            condition["status"] = status

        purchase_invoice = frappe.db.get_all(
            "Purchase Invoice",
            filters=condition,
            fields=[
                "name",
                "supplier",
                "posting_date",
                "status",
                "grand_total",
                "outstanding_amount",
            ],
        )

        if supplier_grp:
            for val in purchase_invoice:
                party_grp = frappe.db.get_value(
                    "Supplier", val["supplier"], "supplier_group"
                )
                if party_grp == supplier_grp:
                    data.append(
                        {
                            "voucher_type": "Purchase Invoice",
                            "voucher_no": val["name"],
                            "party": val["supplier"],
                            "party_group": party_grp,
                            "posting_date": val["posting_date"],
                            "status": val["status"],
                            "total_amount": val["grand_total"],
                            "outstanding_amount": val["outstanding_amount"],
                            "actions": "Actions",
                            "view_items": "View Items",
                        }
                    )

        else:

            for val in purchase_invoice:
                party_grp = frappe.db.get_value(
                    "Supplier", val["supplier"], "supplier_group"
                )

                data.append(
                    {
                        "voucher_type": "Purchase Invoice",
                        "voucher_no": val["name"],
                        "party": val["supplier"],
                        "party_group": party_grp,
                        "posting_date": val["posting_date"],
                        "status": val["status"],
                        "total_amount": val["grand_total"],
                        "outstanding_amount": val["outstanding_amount"],
                        "actions": "Actions",
                        "view_items": "View Items",
                    }
                )

    elif VoucherType == "Delivery Note":
        condition = {
            "docstatus": 1,
            "posting_date": ["between", [From, To]],
        }
        if customer:
            condition["customer"] = customer

        if status:
            condition["status"] = status

        delivery_note = frappe.db.get_all(
            "Delivery Note",
            filters=condition,
            fields=["name", "customer", "posting_date", "status", "grand_total"],
        )

        if customer_grp:
            for val in delivery_note:
                party_grp = frappe.db.get_value(
                    "Customer", val["customer"], "customer_group"
                )
                if party_grp == customer_grp:
                    data.append(
                        {
                            "voucher_type": "Delivery Note",
                            "voucher_no": val["name"],
                            "party": val["customer"],
                            "party_group": party_grp,
                            "posting_date": val["posting_date"],
                            "status": val["status"],
                            "total_amount": val["grand_total"],
                            # "outstanding_amount": val["outstanding_amount"],
                            "actions": "Actions",
                            "view_items": "View Items",
                        }
                    )

        else:

            for val in delivery_note:
                party_grp = frappe.db.get_value(
                    "Customer", val["customer"], "customer_group"
                )

                data.append(
                    {
                        "voucher_type": "Delivery Note",
                        "voucher_no": val["name"],
                        "party": val["customer"],
                        "party_group": party_grp,
                        "posting_date": val["posting_date"],
                        "status": val["status"],
                        "total_amount": val["grand_total"],
                        # "outstanding_amount": val["outstanding_amount"],
                        "actions": "Actions",
                        "view_items": "View Items",
                    }
                )

    elif VoucherType == "Purchase Receipt":
        condition = {
            "docstatus": 1,
            "posting_date": ["between", [From, To]],
        }
        if supplier:
            condition["supplier"] = supplier

        if status:
            condition["status"] = status

        purchase_receipt = frappe.db.get_all(
            "Purchase Receipt",
            filters=condition,
            fields=["name", "supplier", "posting_date", "status", "grand_total"],
        )

        if supplier_grp:
            for val in purchase_receipt:
                party_grp = frappe.db.get_value(
                    "Supplier", val["supplier"], "supplier_group"
                )
                if party_grp == supplier_grp:
                    data.append(
                        {
                            "voucher_type": "Purchase Receipt",
                            "voucher_no": val["name"],
                            "party": val["supplier"],
                            "party_group": party_grp,
                            "posting_date": val["posting_date"],
                            "status": val["status"],
                            "total_amount": val["grand_total"],
                            # "outstanding_amount": val["outstanding_amount"],
                            "actions": "Actions",
                            "view_items": "View Items",
                        }
                    )

        else:

            for val in purchase_receipt:
                party_grp = frappe.db.get_value(
                    "Supplier", val["supplier"], "supplier_group"
                )

                data.append(
                    {
                        "voucher_type": "Purchase Receipt",
                        "voucher_no": val["name"],
                        "party": val["supplier"],
                        "party_group": party_grp,
                        "posting_date": val["posting_date"],
                        "status": val["status"],
                        "total_amount": val["grand_total"],
                        # "outstanding_amount": val["outstanding_amount"],
                        "actions": "Actions",
                        "view_items": "View Items",
                    }
                )

    return columns, data


# sql_query = frappe.db.sql("""
#                select
#                    pinvoice.name,
#                    p.invoice.total_amount,
#                    p.
#                from `tabPurchase Invoice Item` pinvoice
#                left join `tabPurchase Receipt Item` receipt
#                    on pinvoice.name = receipt.purchase_invoice_item
#                    and receipt.docstatus = 1
#                where pinvoice.parent in ("ACC-PINV-2025-00013","ACC-PINV-2025-00010")
#                group by pinvoice.name, pinvoice.item_code
#                having qty >0
#            """, as_dict=1)
