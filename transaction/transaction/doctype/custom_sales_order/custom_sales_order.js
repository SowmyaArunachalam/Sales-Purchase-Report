// Copyright (c) 2025,   and contributors
// For license information, please see license.txt

frappe.ui.form.on("Custom Sales Order", {
	onload: function (frm) {
		frm.set_value("transaction_date", frappe.datetime.get_today());
	},
});

frappe.ui.form.on("Custom Sales Order Item", {
	qty: function (frm, cdt, cdn) {
		child_value(frm, cdt, cdn);
		parent_value(frm, cdt, cdn);
	},
	rate: function (frm, cdt, cdn) {
		child_value(frm, cdt, cdn);
	},
	amount: function (frm, cdt, cdn) {
		parent_value(frm, cdt, cdn);
	},
});

function child_value(frm, cdt, cdn) {
	var row = locals[cdt][cdn];
	let amt = row.rate * row.qty;
	if (frm.doc.delivery_date) {
		row.delivery_date = frm.doc.delivery_date;
		refresh_field("delivery_date", cdn, "items");
	}
	if (row.qty && row.rate) {
		frappe.model.set_value(cdt, cdn, "delivery_date", frm.doc.delivery_date);
		frappe.model.set_value(cdt, cdn, "price_list_rate", row.rate);
		frappe.model.set_value(cdt, cdn, "base_price_list_rate", row.rate);
		frappe.model.set_value(cdt, cdn, "base_rate", row.rate);
		frappe.model.set_value(cdt, cdn, "amount", amt);
		frappe.model.set_value(cdt, cdn, "net_rate", row.rate);
		frappe.model.set_value(cdt, cdn, "base_net_rate", row.rate);
		frappe.model.set_value(cdt, cdn, "net_amount", amt);
		frappe.model.set_value(cdt, cdn, "base_net_amount", amt);
	}
}

function parent_value(frm, cdt, cdn) {
	var row = locals[cdt][cdn];

	console.log(frm.doc);
	let tot_qty = 0;
	let tot_amt = 0;
	console.log("Helllooo");
	frm.doc.items.forEach((element) => {
		console.log(element);
		console.log(element.qty);
		console.log(element.amount);

		tot_amt += element.amount;
		tot_qty += element.qty;
	});
	console.log(tot_qty);
	console.log(tot_amt);

	frm.set_value("total", tot_amt);
	frm.set_value("total_qty", tot_qty);
	frm.set_value("grand_total", tot_amt);
	frm.set_value("rounded_total", tot_amt);
}
