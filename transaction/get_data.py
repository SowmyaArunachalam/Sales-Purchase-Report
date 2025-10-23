import frappe
import json


from frappe.utils import today
current_date = today()

@frappe.whitelist()
def view_items(doctype, doc_name):
    if doctype == "Sales Order":

        item = frappe.db.get_all(
            "Sales Order Item",
            filters={"parent": doc_name},
            fields=["item_code", "item_name", "qty", "rate"],
        )

        query = frappe.db.sql(
            """
            select  sorder.item_code, sum(note.qty) as qty
            from `tabSales Order Item` as sorder
            left join `tabDelivery Note Item` as note
                on sorder.name = note.so_detail
                and note.docstatus = 1
            where sorder.parent = %s
            group by sorder.name, sorder.item_code
        """,
            (doc_name,),
            as_dict=1,
        )

        if query:
            for key1 in item:
                print(key1)
                for key2 in query:
                    if key1["item_code"] == key2["item_code"]:
                        if key2["qty"]:
                            key1["delivered_qty"] = f"Deliveried {round(key2['qty'])}"
                        else:
                            key1["delivered_qty"] = "Pending"
                    print(key2)
        return item

    elif doctype == "Sales Invoice":
        item = frappe.db.get_all(
            "Sales Invoice Item",
            filters={"parent": doc_name},
            fields=["item_code", "item_name", "qty", "rate"],
        )
        query = frappe.db.sql(
            """
            select  sinvoice.item_code, sum(note.qty) as qty
            from `tabSales Invoice Item` as sinvoice
            left join `tabDelivery Note Item` as note
                on sinvoice.name = note.si_detail
                and note.docstatus = 1
            where sinvoice.parent = %s
            group by sinvoice.name, sinvoice.item_code
        """,
            (doc_name,),
            as_dict=1,
        )

        if query:
            for key1 in item:
                print(key1)
                for key2 in query:
                    if key1["item_code"] == key2["item_code"]:
                        if key2["qty"]:
                            key1["delivered_qty"] = f"Deliveried {round(key2['qty'])}"
                        else:
                            key1["delivered_qty"] = "Pending"
                    print(key2)

        return item
    elif doctype == "Purchase Order":
        item = frappe.db.get_all(
            "Purchase Order Item",
            filters={"parent": doc_name},
            fields=["item_code", "item_name", "qty", "rate"],
        )
        query = frappe.db.sql(
            """
            select  porder.item_code, sum(receipt.qty) as qty
            from `tabPurchase Order Item` porder
            left join `tabPurchase Receipt Item` receipt
                on porder.name = receipt.purchase_order_item
                and receipt.docstatus = 1
            where porder.parent = %s 
            group by porder.name, porder.item_code
        """,
            (doc_name,),
            as_dict=1,
        )

        if query:
            for key1 in item:
                # print(key1)
                for key2 in query:
                    if key1["item_code"] == key2["item_code"]:
                        if key2["qty"]:
                            key1["delivered_qty"] = f"Received {round(key2['qty'])}"
                        else:
                            key1["delivered_qty"] = "Pending"
                    # print(key2)
        # print(item)
        return item

    elif doctype == "Purchase Invoice":
        item = frappe.db.get_all(
            "Purchase Invoice Item",
            filters={"parent": doc_name},
            fields=["item_code", "item_name", "qty", "rate"],
        )
        query = frappe.db.sql(
            """
            select  pinvoice.item_code, sum(receipt.qty) as qty
            from `tabPurchase Invoice Item` pinvoice
            left join `tabPurchase Receipt Item` receipt
                on pinvoice.name = receipt.purchase_invoice_item 
                and receipt.docstatus = 1
            where pinvoice.parent = %s
            group by pinvoice.name, pinvoice.item_code
        """,
            (doc_name,),
            as_dict=1,
        )

        if query:
            for key1 in item:
                for key2 in query:
                    if key1["item_code"] == key2["item_code"]:
                        if key2["qty"]:
                            key1["delivered_qty"] = f"Received {round(key2['qty'])}"
                        else:
                            key1["delivered_qty"] = "Pending"
                    # print(key2)
        # print(item)
        return item

    elif doctype == "Delivery Note":
        item = frappe.db.get_all(
            "Delivery Note Item",
            filters={"parent": doc_name},
            fields=["item_code", "item_name", "qty", "rate"],
        )

        return item

    elif doctype == "Purchase Receipt":
        item = frappe.db.get_all(
            "Purchase Receipt Item",
            filters={"parent": doc_name},
            fields=["item_code", "item_name", "qty", "rate"],
        )

        print(item)
        return item


@frappe.whitelist()
def so_data(doc):
    doc = json.loads(doc)
    doc = frappe._dict(doc)
    print(doc)
    if doc.voucher_type == "Sales Order":

        item = frappe.db.get_all(
            "Sales Order Item",
            filters={"parent": doc.voucher_no},
            fields=[
                "item_code",
                "item_name",
                "qty",
                "rate",
                "delivery_date",
                "uom",
                "conversion_factor",
            ],
        )
        return item

    elif doc.voucher_type == "Purchase Order":

        item = frappe.db.get_all(
            "Purchase Order Item",
            filters={"parent": doc.voucher_no},
            fields=[
                "item_code",
                "item_name",
                "qty",
                "rate",
                "schedule_date",
                "uom",
                "conversion_factor",
            ],
        )
        return item
    elif doc.voucher_type == "Purchase Invoice":
        item = frappe.db.get_all(
            "Purchase Invoice Item",
            filters={"parent": doc.voucher_no},
            fields=[
                "item_code",
                "item_name",
                "qty",
                "rate",
                "purchase_order",
                "po_detail",
                "uom",
                "conversion_factor"
            ],
        )
        return item
    
    elif doc.voucher_type == "Sales Invoice":
        item = frappe.db.get_all(
            "Sales Invoice Item",
            filters={"parent": doc.voucher_no},
            fields=[
                "name",
                "item_code",
                "item_name",
                "qty",
                "rate",
                "sales_order",
                "so_detail",
                "sales_invoice_item",
                "uom",
                "conversion_factor"
            ],
        )
        return item
    elif doc.voucher_type == "Purchase Receipt":
        item = frappe.db.get_all(
            "Purchase Receipt Item",
            filters={"parent": doc.voucher_no},
            fields=[
                "name",
                "item_code",
                "item_name",
                "qty",
                "rate",
                "purchase_order",
                "purchase_invoice",
                "purchase_order_item",
                "uom",
                "conversion_factor"
            ],
        )
        return item
    elif doc.voucher_type == "Delivery Note":
        item = frappe.db.get_all(
            "Delivery Note Item",
            filters={"parent": doc.voucher_no},
            fields=[
                "name",
                "item_code",
                "item_name",
                "qty",
                "rate",
                "against_sales_invoice",
                "si_detail",
                "so_detail",
                "uom",
                "conversion_factor"
            ],
        )
        print(item)
        return item

@frappe.whitelist()
def debit_note(dtype, item1, args):
    doc = frappe.get_doc(dtype, item1)
    args = frappe.parse_json(args)
    # print(args)
    # doc = json.loads(doc)
    # doc = frappe._dict(doc)
    print(doc.items)
    # print(doc)
    doc1 = frappe.new_doc(doc.doctype)
    
    if doc.doctype == "Sales Invoice":
        doc1.customer = doc.customer
        doc1.selling_price_list = "Standard Selling"
        doc1.select_print_heading = "Credit Note"
        
    elif doc.doctype == "Purchase Invoice":
        doc1.supplier = doc.supplier
        doc1.buying_price_list = "Standard Buying"
        doc1.select_print_heading = "Debit Note"
        
    elif doc.doctype == "Purchase Receipt":
        doc1.supplier = doc.supplier
        doc1.buying_price_list = "Standard Buying"
        
    elif doc.doctype == "Delivery Note":
        doc1.customer = doc.customer
        doc1.selling_price_list = "Standard Selling"
        
    doc1.return_against = doc.name
    doc1.company = doc.company
    doc1.posting_date = current_date
    doc1.is_return = 1
    doc1.update_outstanding_for_self = 1
    doc1.update_billed_amount_in_purchase_receipt = 1
    doc1.currency = "INR"
    print(args.table)
    for item in args.table:
        new_dict = {
                "item_code": item["item_code"],
                "item_name": item["item_name"],
                "qty": item["qty"],
                "uom": item["uom"],
                "rate": item["rate"],
        }
        print(new_dict)
        if type == "Sales Invoice":
            new_dict.update({"sales_order":  item["sales_order"], "so_detail": item["so_detail"], "sales_invocie_item": item["sales_invocie_item"]})
        elif type == "Purchase Invoice":
            new_dict.update({"purchase_order": item["purchase_order"], "po_detail": item["po_detail"], "purchase_invoice_item": item["purchase_invoice_item"]})
        elif type == "Purchase Receipt":
            new_dict.update({"purchase_order": item["purchase_order"], "purchase_invoice": item["purchase_invoice"], "purchase_order_item": item["purchase_order_item"], "purchase_receipt_item": item["purchase_receipt_item"]})
        elif type == "Delivery Note":
            new_dict.update({"against_sales_invoice": item["against_sales_invoice"], "si_detail": item["si_detail"], "dn_detail": item["dn_detail"]})

        doc1.append("items", new_dict)
    doc1.insert()
    return doc1.name


# @frappe.whitelist()
# def pur_invoice(id):
#     # data = frappe.get_doc("Purchase Order", id)
#     doc1 = get_mapped_purchase_invoice(id)
#     doc1.insert()


@frappe.whitelist()
def checked_items(type, selected_value):
    selected_value = frappe.parse_json(selected_value)
    sql_query = 0
    id_list = tuple(s["voucher_no"] for s in selected_value)
    placeholders = ", ".join(["%s"] * len(id_list))
    if type == "Purchase Order":
        sql_query = f"""select
                    porder.name,
                    porder.item_code,
                    porder.item_name,
                    porder.rate,
                    porder.qty - ifnull(sum(invoice.qty), 0) as qty,
                    porder.uom
                from `tabPurchase Order Item` porder
                left join `tabPurchase Invoice Item` invoice
                    on porder.name = invoice.po_detail
                    and invoice.docstatus = 1
                where porder.parent in ({placeholders})
                group by porder.name, porder.item_code
                having qty >0"""

    elif type == "Sales Order":
        sql_query = f"""
                select
                    sorder.name,
                    sorder.item_code,
                    sorder.item_name,
                    sorder.rate,
                    sorder.qty - ifnull(sum(invoice.qty), 0) as qty,
                    sorder.uom
                    
                from `tabSales Order Item` sorder
                left join `tabSales Invoice Item` invoice
                    on sorder.name = invoice.so_detail
                    and invoice.docstatus = 1
                where sorder.parent in ({placeholders})
                group by sorder.name, sorder.item_code
                having qty >0
            """

    elif type == "Sales Invoice":
        sql_query = f"""
                select
                    sinvoice.name,
                    sinvoice.item_code,
                    sinvoice.item_name,
                    sinvoice.rate,
                    sinvoice.qty - ifnull(sum(note.qty), 0) as qty,
                    sinvoice.uom
                    
                from `tabSales Invoice Item` sinvoice
                left join `tabDelivery Note Item` note
                    on sinvoice.name = note.si_detail
                    and note.docstatus = 1
                where sinvoice.parent in ({placeholders})
                group by sinvoice.name, sinvoice.item_code
                having qty >0
            """
    elif type == "Purchase Invoice":
        sql_query = f"""
                select
                    pinvoice.name,
                    pinvoice.item_code,
                    pinvoice.item_name,
                    pinvoice.rate,
                    pinvoice.qty - ifnull(sum(receipt.qty), 0) as qty,
                    pinvoice.uom,
                    pinvoice.po_detail,
                    pinvoice.purchase_order
                    
                from `tabPurchase Invoice Item` pinvoice
                left join `tabPurchase Receipt Item` receipt
                    on pinvoice.name = receipt.purchase_invoice_item
                    and receipt.docstatus = 1
                where pinvoice.parent in ({placeholders})
                group by pinvoice.name, pinvoice.item_code
                having qty >0
            """

    query = frappe.db.sql(sql_query, id_list, as_dict=1)
    print(query)
    # l=[i for i in query]
    # print(l)
    if query == []:
        frappe.throw("All order created.")

    return query


@frappe.whitelist()
def new_invoice(type, item1, args=None):
    doc = frappe.get_doc(type, item1)
    # doc = json.loads(doc)
    # doc = frappe._dict(doc)
    doc = frappe.parse_json(doc)
    # args =json.loads(args)
    # args = frappe._dict(args)
    args = frappe.parse_json(args)

    # final
    if type == "Purchase Order":
        doc1 = frappe.new_doc("Purchase Invoice")
        doc1.supplier = doc.supplier
        doc1.buying_price_list = doc.buying_price_list

    else:
        doc1 = frappe.new_doc("Sales Invoice")
        doc1.customer = doc.customer
        doc1.selling_price_list = doc.selling_price_list

    # company = frappe.get_value("Company",doc.company,"default_income_account")

    doc1.posting_date = current_date
    doc1.due_date = current_date
    doc1.currency = doc.currency
    doc1.set_posting_time = 1

    print(doc1)

    for item in args.table:

        new_dict = {
            "item_code": item["item_code"],
            "item_name": item["item_name"],
            "qty": item["qty"],
            "uom": item["uom"],
            "rate": item["rate"]
        }
        print(new_dict)
        if type == "Sales Order":
            new_dict.update({"sales_order": doc.name, "so_detail": item["name"]})
        elif type == "Purchase Order":
            new_dict.update({"purchase_order": doc.name, "po_detail": item["name"]})

        doc1.append("items", new_dict)
        print(new_dict)

    doc1.total_qty = doc.total_qty
    doc1.total = doc.total
    doc1.grand_total = doc.grand_total
    doc1.rounding_adjustment = doc.rounding_adjustment
    doc1.rounded_total = doc.rounded_total
    doc1.in_words = doc.in_words
    doc1.insert()
    return doc1.name

# @frappe.whitelist()
# def del_note(type):
#     doc1 = frappe.get_doc(type,id)
#     new_value = make_delivery_note(doc1)
#     # print(new_value)
#     new_value.insert()
#     return new_value

@frappe.whitelist()
def del_note(type, item1, args=None):
    doc = frappe.get_doc(type, item1)
    doc = frappe.parse_json(doc)
    args = frappe.parse_json(args)

    doc1 = frappe.new_doc("Delivery Note")
    doc1.customer = doc.customer
    doc1.selling_price_list = doc.selling_price_list
    # company = frappe.get_value("Company",doc.company,"default_income_account")
    doc1.company = doc.company
    doc1.posting_date = current_date
    doc1.set_posting_time = 1
    doc1.due_date = doc.due_date
    doc1.currency = doc.currency
    # doc1.set_posting_time = 1
    doc1.selling_price_list = "Standard Selling"
    print(doc1)

    for item in args.table:
        print(item)
        doc1.append(
            "items",
            {
                "item_code": item["item_code"],
                "item_name": item["item_name"],
                "qty": item["qty"],
                "uom": item["uom"],
                # "price_list_rate":item['price_list_rate'],
                # "base_price_list_rate":item['base_price_list_rate'],
                "rate": item["rate"],
                # "amount":item['amount'],
                # "cost_center": item['cost_center'],
                "purchase_order": item["purchase_order"],
                "po_detail": item["po_detail"],
            },
        )

    doc1.total_qty = doc.total_qty
    doc1.total = doc.total
    doc1.grand_total = doc.grand_total
    doc1.rounding_adjustment = doc.rounding_adjustment
    doc1.rounded_total = doc.rounded_total
    doc1.in_words = doc.in_words
    doc1.insert()
    # doc1.submit()
    # frappe.set_route("Form", "Sales Invoice", doc1.name)
    print(doc.name)
    return doc1.name


@frappe.whitelist()
def pur_receipt(type, item1, args=None):
    doc = frappe.get_doc(type, item1)
    doc = frappe.parse_json(doc)
    args = frappe.parse_json(args)

    doc1 = frappe.new_doc("Purchase Receipt")
    doc1.supplier = doc.supplier
    doc1.company = doc.company
    doc1.posting_date = current_date
    doc1.set_posting_time = 1
    # doc1.selling_price_list = doc.selling_price_list
    # company = frappe.get_value("Company",doc.company,"default_income_account")

    doc1.due_date = current_date
    doc1.currency = doc.currency
    doc1.set_posting_time = 1
    doc1.selling_price_list = "Standard Selling"
    print(doc1)

    for item in args.table:
        print(item)
        doc1.append(
            "items",
            {
                "item_code": item["item_code"],
                "item_name": item["item_name"],
                "qty": item["qty"],
                "uom": item["uom"],
                "rate": item["rate"],
                "purchase_invoice": doc.name,
                "purchase_invoice_item": item["name"],
                "purchase_order_item": item["po_detail"],
                "purchase_order": item["purchase_order"],
            },
        )

    doc1.total_qty = doc.total_qty
    doc1.total = doc.total
    doc1.grand_total = doc.grand_total
    doc1.rounding_adjustment = doc.rounding_adjustment
    doc1.rounded_total = doc.rounded_total
    doc1.in_words = doc.in_words
    doc1.insert()
    # doc1.submit()
    # frappe.set_route("Form", "Sales Invoice", doc1.name)
    print(doc1.name)
    return doc1.name


@frappe.whitelist()
def payment(type, selected_value):
    selected_value = frappe.parse_json(selected_value)
    # sql_query = 0
    id_list = tuple(s["voucher_no"] for s in selected_value)

    print(id_list)

    doc = frappe.get_doc(type, id_list[0])

    if doc.status == "Paid" and len(id_list) == 0:
        frappe.throw("Paid full amount...")
    # doc = frappe.parse_json(doc)
    # args = frappe.parse_json(args)
    doc1 = frappe.new_doc("Payment Entry")

    if type == "Sales Invoice":
        doc1.party_type = "Customer"
        doc1.payment_type = "Receive"
        doc1.party_name = doc.customer_name
        doc1.party = doc.customer
        doc1.paid_from = "Debtors - G"
        doc1.paid_to = "Cash - G"
        doc1.paid_from_account_type = "Receivable"
        doc1.paid_to_account_type = "Cash"

    if type == "Purchase Invoice":
        doc1.party_type = "Supplier"
        doc1.payment_type = "Pay"
        doc1.party_name = doc.supplier_name
        doc1.party = doc.supplier
        doc1.paid_from = "Cash - G"
        doc1.paid_to = "Creditors - G"
        doc1.paid_from_account_type = "Cash"
        doc1.paid_to_account_type = "Payable"

    print(doc)

    doc1.company = doc.company
    doc1.posting_date = current_date
    doc1.mode_of_payment = "Cash"
    doc1.paid_from_account_currency = "INR"
    doc1.paid_to_account_currency = "INR"
    doc1.source_exchange_rate = 1
    doc1.target_exchange_rate = 1
    total = 0
    outstanding_total = 0
    for id in id_list:
        doc = frappe.get_doc(type, id)
        # doc = frappe.parse_json(doc)
        if doc.outstanding_amount == 0:
            continue
        doc1.append(
            "references",
            {
                "reference_doctype": type,
                "reference_name": id,
                "total_amount": doc.total,
                "exchange_rate": 1,
                "outstanding_amount": doc.outstanding_amount,
                "allocated_amount": doc.outstanding_amount,
            },
        )

        total += doc.total
        outstanding_total += doc.outstanding_amount
    # print(doc1.meta.get_table_fields())

    doc1.paid_amount = outstanding_total or 0
    doc1.received_amount = total

    doc1.insert()

    return doc1.name









# sql_query = f"""select
#                     porder.name,
#                     porder.item_code,
#                     porder.item_name,
#                     porder.rate,
#                     porder.qty - ifnull(sum(invoice.qty), 0) as qty,
#                     porder.uom
#                 from `tabPurchase Order Item` porder
#                 left join `tabPurchase Invoice Item` invoice
#                     on porder.name = invoice.po_detail
#                     and invoice.docstatus = 1
#                 where porder.parent in ({placeholders})
#                 group by porder.name, porder.item_code
#                 having qty >0"""
                
                
# query = (
#     frappe.qb.from(PurchaseOrderItem)
#     .left_join(PurchaseInvoiceItem)
#     .on(PurchaseOrderItem.name = PurchaseInvoiceItem.podetail and PurchaseInvoiceItem.docstatus = 1)
#     .select(PurchaseOrderItem.name,
#             PurchaseOrderItem,item_code,
#             PurchaseOrderItem.item_name,
#             PurchaseOrderItem.rate,
#             PurchaseOrderItem.qty - PurchaseInvoiceItem.qty as qty,
#             PurchaseOrderItem.uom)
#     .where(PurchaseOrderItem.parent = "")
#     .group_by(PurchaseOrderItem.name, PurchaseOrderItem.item_code)
#     .having(qty > 0)
# )