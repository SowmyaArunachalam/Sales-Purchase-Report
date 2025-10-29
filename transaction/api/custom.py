import frappe
from frappe import _
import json


@frappe.whitelist(allow_guest=True)
def Custom_record(obj_value=None):
    l = []
    # data = frappe._dict(json.loads(obj_value))
    try:
        data = json.loads(obj_value)
    except:
        frappe.throw("Error in Json...")
    # return data

    for obj_data in data:

        query = frappe.db.sql(
            "select new_id from `tabCustom Sales Order` where new_id = %s ",
            obj_data["new_id"],
            as_dict=1
        )

        if query:
            frappe.throw("Already exists")

        doc1 = frappe.new_doc("Custom Sales Order")
        doc1.new_id = obj_data["new_id"]
        doc1.transaction_date = obj_data["transaction_date"]
        doc1.delivery_date = obj_data["delivery_date"]
        doc1.customer = obj_data["customer"]
        doc1.company = obj_data["company"]
        doc1.order_type = "Sales"
        doc1.currency = "INR"
        doc1.price_list = "Standard Selling"
        tot = 0
        qty = 0
        for item in obj_data["items"]:
            amt = item["rate"] * item["qty"]
            tot += amt
            qty += item["qty"]
            doc1.append(
                "items",
                {
                    "item_code": item["item_code"],
                    "item_name": item.get("item_name"),
                    "delivery_date": obj_data["delivery_date"],
                    "qty": item["qty"],
                    "uom": "Nos",
                    "uom_conversion_factor": 1,
                    "rate": item["rate"],
                    "amount": amt,
                    "parent": doc1.name,
                    "parenttype": "Sales Order",
                    "price_list_rate": item["rate"],
                    "base_price_list_rate": item["rate"],
                    "base_rate": item["rate"],
                    "amount": amt,
                    "net_rate": item["rate"],
                    "base_net_rate": item["rate"],
                    "net_amount": amt,
                    "base_net_amount": amt
                },
            )
        doc1.total_qty = qty
        doc1.total = tot
        doc1.tototal_qtytal = tot
        doc1.grand_total = tot
        doc1.rounded_total = tot

        l.append(doc1)
        doc1.save()

    return l


# @frappe.whitelist(allow_guest=True)
def Create_order():

    # obj_data = json.loads(obj_value)
    
    query = frappe.db.get_all("Custom Sales Order", filters = {
        'order_status':'Order not Created'}, pluck='name')
    
    
    for i in query:
        obj_value = frappe.get_doc("Custom Sales Order", i)
        obj_data = obj_value.as_dict()
        # return obj_data
        # obj_data = json.loads(obj_value)
        print("------", i)
        get_user = frappe.db.sql(
            "Select name from `tabCustomer` where customer_name = %s", obj_data["customer"]
        )
        
        if not get_user:
            doc = frappe.get_doc(
                {
                    "doctype": "Customer",
                    "customer_name": obj_data["customer"],
                    "customer_type": "Company",
                }
            )
            doc.insert()

        frappe.db.set_value("Custom Sales Order", i, "order_status", "Order Delivered")

        doc1 = frappe.new_doc("Sales Order")
        doc1.transaction_date = obj_data["transaction_date"]
        doc1.delivery_date = obj_data["delivery_date"]
        doc1.customer = obj_data["customer"]
        doc1.company = obj_data["company"]
        doc1.order_type = "Sales"
        doc1.currency = "INR"
        doc1.price_list = "Standard Selling"
        tot = 0
        qty = 0
        for item in obj_data["items"]:
            get_item = frappe.db.sql(
                "Select name from `tabItem` where name = %s ", item["item_name"]
            )

            if not get_item:
                frappe.throw("Item not in Warehouse.")

            amt = item["rate"] * item["qty"]
            tot += amt
            qty += item["qty"]
            doc1.append(
                "items",
                {
                    "item_code": item["item_code"],
                    "item_name": item["item_name"],
                    "delivery_date": obj_data["delivery_date"],
                    "qty": item["qty"],
                    "uom": "Nos",
                    "uom_conversion_factor": 1,
                    "rate": item["rate"],
                    "amount": amt,
                    "parent": doc1.name,
                    "parenttype": "Sales Order",
                    "price_list_rate": item["rate"],
                    "base_price_list_rate": item["rate"],
                    "base_rate": item["rate"],
                    "amount": amt,
                    "net_rate": item["rate"],
                    "base_net_rate": item["rate"],
                    "net_amount": amt,
                    "base_net_amount": amt,
                },
            )
        doc1.total_qty = qty
        doc1.total = tot
        doc1.tototal_qtytal = tot
        doc1.grand_total = tot
        doc1.rounded_total = tot
        doc1.insert()
        print("Created--------")
        # return doc1
