// Copyright (c) 2025,   and contributors
// For license information, please see license.txt
let new_data = {};
// let fields = [
// 		{
// 			fieldtype: "Data",
// 			fieldname: "docname",
// 			read_only: 0,
// 			hidden: 1,
// 		},
// 		{
// 			fieldname: "item_code",
// 			fieldtype: "Link",
// 			in_list_view: 1,
// 			label: "Item Code",
// 			read_only: 1,
// 			disabled: 0,
// 		},
// 		{
// 			fieldname: "item_name",
// 			fieldtype: "Link",
// 			in_list_view: 1,
// 			label: "Item Name",
// 			read_only: 1,
// 			disabled: 0,
// 		},
// 		{
// 			fieldtype: "Link",
// 			fieldname: "uom",
// 			options: "UOM",
// 			read_only: 1,
// 			label: __("UOM"),
// 			reqd: 1,
// 		},
// 		{
// 			fieldname: "qty",
// 			fieldtype: "Float",
// 			label: "Quantity",
// 			in_list_view: 1,
// 			default: 0,
// 			read_only: 0,
// 		},
// 		{
// 			fieldname: "rate",
// 			fieldtype: "Currency",
// 			in_list_view: 1,
// 			label: "Rate(INR)",
// 			read_only: 1,
// 			default: 0,
// 		},
// 	]
frappe.query_reports["Transaction List"] = {
	get_datatable_options(options) {
		return Object.assign(options, {
			checkboxColumn: true,
		});
	},

	filters: [
		{
			fieldname: "voucher_type",
			label: "Voucher Type",
			fieldtype: "Select",
			options: [
				"Sales Order",
				"Purchase Order",
				"Sales Invoice",
				"Purchase Invoice",
				"Delivery Note",
				"Purchase Receipt",
			],
			reqd: 0,
			on_change: function (query_report) {
				console.log("Type --------------");
				query_report.page.clear_actions_menu();

				//to get checked items
				action_list(query_report);
				frappe.query_report.refresh();

				//filter for status
				let filters = frappe.query_report.filters;
				let dtype = frappe.query_report.get_filter_value("voucher_type");
				let options = {
					"Sales Order": [
						"On Hold",
						"To Deliver and Bill",
						"To Bill",
						"To Deliver",
						"Completed",
					],
					"Sales Invoice": [
						"Return",
						"Credit Note Issued",
						"Paid",
						"Partly Paid",
						"Unpaid",
						"Unpaid and Discounted",
						"Partly Paid and Discounted",
						"Overdue and Discounted",
						"Overdue",
						"Internal Transfer",
					],
					"Purchase Order": [
						"On Hold",
						"To Receive and Bill",
						"To Bill",
						"To Receive",
						"Completed",
						"Delivered",
					],
					"Purchase Invoice": [
						"Return",
						"Debit Note Issued",
						"Paid",
						"Partly Paid",
						"Unpaid",
						"Overdue",
						"Internal Transfer",
					],
					"Delivery Note": ["To Bill", "Completed", "Return Issued"],
					"Purchase Receipt": ["Partly Billed", "To Bill", "Completed", "Return Issued"],
				};
				filters.forEach((d) => {
					if (d.fieldname == "status") {
						d.df.options = options[dtype].join("\n");
						d.set_input(d.df.options);
					}
				});
				frappe.query_report.refresh();
			},
		},
		{
			fieldname: "from",
			label: "From",
			fieldtype: "Date",
			reqd: 1,
		},
		{
			fieldname: "to",
			label: "To",
			fieldtype: "Date",
			reqd: 1,
		},
		{
			fieldname: "status",
			label: "Status",
			fieldtype: "Select",
			reqd: 0,
		},
		{
			fieldname: "customer",
			label: "Customer",
			fieldtype: "Link",
			reqd: 0,
			options: "Customer",
			depends_on:
				'eval: ["Sales Order", "Sales Invoice", "Delivery Note"].includes(doc.voucher_type)',
		},
		{
			fieldname: "customer_group",
			label: "Customer Group",
			fieldtype: "Link",
			reqd: 0,
			options: "Customer Group",
			depends_on:
				'eval: ["Sales Order", "Sales Invoice", "Delivery Note"].includes(doc.voucher_type)',
		},
		{
			fieldname: "supplier",
			label: "Supplier",
			fieldtype: "Link",
			reqd: 0,
			options: "Supplier",
			depends_on:
				'eval: ["Purchase Order", "Purchase Invoice", "Purchase Receipt"].includes(doc.voucher_type)',
		},
		{
			fieldname: "supplier_group",
			label: "Supplier Group",
			fieldtype: "Link",
			reqd: 0,
			options: "Supplier Group",
			depends_on:
				'eval: ["Purchase Order", "Purchase Invoice", "Purchase Receipt"].includes(doc.voucher_type)',
		},
	],

	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		const key = data.voucher_no;
		new_data[key] = data;

		if (column.fieldname === "actions") {
			value = `
						<button class="btn mb-2 btn-outline-dark btn-light btn-xs"
							
							onclick=" so_actions('${key}')">

							Update Items
						</button>
						`;
		}

		if (column.fieldname === "view_items") {
			value = `
						<button class="btn mb-2 btn-outline-dark btn-light btn-xs"
							onclick=" show_items('${data.voucher_type}','${data.voucher_no}')
							">
							View Items
						</button>
						`;
		}
		return value;
	},
};

function so_actions(key) {
	let data = new_data[key];
	list_item = [];

	let fields = [
		{
			fieldtype: "Data",
			fieldname: "docname",
			read_only: 0,
			hidden: 1,
		},
		{
			fieldname: "item_code",
			fieldtype: "Link",
			in_list_view: 1,
			label: "Item Code",
			read_only: 0,
			disabled: 0,
		},
		{
			fieldtype: "Link",
			fieldname: "uom",
			options: "UOM",
			read_only: 0,
			label: __("UOM"),
			reqd: 1,
		},
		{
			fieldname: "qty",
			fieldtype: "Float",
			label: "Quantity",
			in_list_view: 1,
			default: 0,
			read_only: 0,
		},

		{
			fieldname: "rate",
			fieldtype: "Currency",
			in_list_view: 1,
			label: "Rate(INR)",
			read_only: 0,
			default: 0,
		},
	];

	if (data.voucher_type == "Sales Order" || data.voucher_type == "Purchase Order") {
		fields.splice(2, 0, {
			fieldtype: "Date",
			fieldname: data.voucher_type == "Sales Order" ? "delivery_date" : "schedule_date",
			in_list_view: 1,
			label: data.voucher_type == "Sales Order" ? __("Delivery Date") : __("Reqd by date"),
			reqd: 1,
		});
		fields.splice(3, 0, {
			fieldtype: "Float",
			fieldname: "conversion_factor",
			label: __("Conversion Factor"),
		});
	}

	frappe.call({
		method: "transaction.get_data.so_data",

		args: {
			doc: data,
		},
		callback: function (r) {
			let query = r.message;

			if (r.message) {
				query.forEach((element) => {
					list_item.push({
						docname: element.name,
						name: element.name,
						item_code: element.item_code,
						item_name: element.item_name,
						qty: element.qty,
						rate: element.rate,
						schedule_date: element.schedule_date,
						delivery_date: element.delivery_date,
						uom: element.uom,
					});
				});
			}

			let dialog = new frappe.ui.Dialog({
				title: "Item Table",
				size: "large",

				fields: [
					{
						label: "Table",
						fieldname: "table",
						fieldtype: "Table",
						cannot_add_rows: true,
						in_place_edit: false,
						data: query,
						fields: fields,
					},
				],

				primary_action_label: "Submit",
				primary_action(values) {
					debugger;
					frappe.call({
						method: "erpnext.controllers.accounts_controller.update_child_qty_rate",
						freeze: true,

						args: {
							parent_doctype: data.voucher_type,

							trans_items: values.table,

							parent_doctype_name: data.voucher_no,

							child_docname: "items",
						},

						callback: function (r) {
							frappe.query_report.refresh();
							console.log("Updated");
						},
					});
					dialog.hide();
				},
			});
			dialog.show();
		},
	});
}

function show_items(type, doc_name) {
	let list_item = [];
	frappe.call({
		method: "transaction.get_data.view_items",

		args: {
			doctype: type,
			doc_name: doc_name,
		},

		callback: function (r) {
			let query = r.message;

			if (r.message) {
				console.log(query);
				query.forEach((element) => {
					list_item.push({
						item_code: element.item_code,
						item_name: element.item_name,
						qty: element.qty,
						rate: element.rate,
						status: "Pending",
					});
				});
			}

			let dialog = new frappe.ui.Dialog({
				title: "Item Table",
				size: "extra-large",

				fields: [
					{
						label: "Table",
						fieldname: "table",
						fieldtype: "Table",
						cannot_add_rows: true,
						in_place_edit: false,
						cannot_delete_rows: true,
						cannot_delete_all_rows: true,
						data: query,
						fields: [
							{
								fieldname: "item_code",
								fieldtype: "Data",
								in_list_view: 1,
								label: "Item Code",
								read_only: 1,
							},
							{
								fieldname: "item_name",
								fieldtype: "Data",
								label: "Item Name",
								in_list_view: 1,
								read_only: 1,
							},
							{
								fieldname: "qty",
								fieldtype: "Data",
								label: "Quantity",
								in_list_view: 1,
								read_only: 1,
							},
							{
								fieldname: "rate",
								fieldtype: "Float",
								in_list_view: 1,
								label: "Rate(INR)",
								read_only: 1,
							},
							{
								fieldname: "delivered_qty",
								fieldtype: "Data",
								in_list_view: 1,
								label: "Delivery/Received",
								read_only: 1,
							},
						],
					},
				],
			});
			dialog.show();
		},
	});
}
function item_dialog(report, items_method, op_method, creation_type) {
	let doc_type = report.get_filter_value("voucher_type");

	let checked_rows_indexes = report.datatable.rowmanager.getCheckedRows();
	let checked_rows = checked_rows_indexes.map((i) => report.data[i]);
	fst_item = checked_rows[0];

	new_l = [];

	checked_rows.forEach((person) => {
		if (person["party"] != fst_item["party"]) {
			frappe.throw("Party should be same.");
		}
	});

	frappe.call({
		method: items_method,
		args: {
			type: doc_type,
			selected_value: checked_rows,
		},
		callback: function (r) {
			let query = r.message;

			if (r.message) {
				query.forEach((element) => {
					new_l.push({
						name: element.name,
						item_code: element.item_code,
						item_name: element.item_name,
						qty: element.qty,
						rate: element.rate,
						uom: element.uom,
					});
				});
			}

			let dialog = new frappe.ui.Dialog({
				title: "Item Table",
				size: "large",

				fields: [
					{
						label: "Table",
						fieldname: "table",
						fieldtype: "Table",
						cannot_add_rows: true,
						in_place_edit: false,
						data: query,
						fields: [
							{
								fieldtype: "Data",
								fieldname: "docname",
								read_only: 0,
								hidden: 1,
							},
							{
								fieldname: "item_code",
								fieldtype: "Link",
								in_list_view: 1,
								label: "Item Code",
								read_only: 1,
								disabled: 0,
							},
							{
								fieldname: "item_name",
								fieldtype: "Link",
								in_list_view: 1,
								label: "Item Name",
								read_only: 1,
								disabled: 0,
							},
							{
								fieldtype: "Link",
								fieldname: "uom",
								options: "UOM",
								read_only: 1,
								label: __("UOM"),
								reqd: 1,
							},
							{
								fieldname: "qty",
								fieldtype: "Float",
								label: "Quantity",
								in_list_view: 1,
								default: 0,
								read_only: 0,
							},
							{
								fieldname: "rate",
								fieldtype: "Currency",
								in_list_view: 1,
								label: "Rate(INR)",
								read_only: 1,
								default: 0,
							},
						],
					},
				],

				primary_action_label: "Submit",
				primary_action() {
					console.log(dialog.get_values());
					frappe.call({
						method: op_method,
						args: {
							type: fst_item["voucher_type"],
							item1: fst_item["voucher_no"],
							args: dialog.get_values(),
						},
						callback: function (r) {
							if (r.message) {
								frappe.set_route("Form", creation_type, r.message);
							}
						},
					});
					dialog.hide();
				},
			});
			dialog.show();
		},
	});
}

function action_list(report) {
	let doc_type = report.get_filter_value("voucher_type");
	let items_method = "transaction.get_data.checked_items";

	if (doc_type === "Sales Order" || doc_type === "Purchase Order") {
		let op_method = "transaction.get_data.new_invoice";
		report.page.add_action_item(__("Create Invoice"), function () {
			if (doc_type === "Sales Order") {
				item_dialog(report, items_method, op_method, "Sales Invoice");
			} else {
				item_dialog(report, items_method, op_method, "Purchase Invoice");
			}
		});
	} else if (doc_type === "Sales Invoice") {
		report.page.add_action_item(__("Delivery Note"), function () {
			let op_method = "transaction.get_data.del_note";
			item_dialog(report, items_method, op_method, "Delivery Note");
		});
		pay_entry(report);
	} else if (doc_type === "Purchase Invoice") {
		report.page.add_action_item(__("Purchase Receipt"), function () {
			let op_method = "transaction.get_data.pur_receipt";
			item_dialog(report, items_method, op_method, "Purchase Receipt");
		});
		pay_entry(report);
	}
}

function pay_entry(report) {
	report.page.add_action_item(__("Payment Entry"), function () {
		let checked_rows_indexes = report.datatable.rowmanager.getCheckedRows();
		let checked_rows = checked_rows_indexes.map((i) => report.data[i]);
		fst_item = checked_rows[0];
		console.log(checked_rows);
		new_l = [];
		console.log(fst_item["voucher_type"]);

		console.log("--------------------");
		checked_rows.forEach((person) => {
			if (person["party"] != fst_item["party"]) {
				frappe.throw("Party should be same.");
			}
		});

		frappe.call({
			method: "transaction.get_data.payment",
			args: {
				type: fst_item["voucher_type"],
				selected_value: checked_rows,
			},
			callback: function (r) {
				let query = r.message;
				if (r.message) {
					frappe.set_route("Form", "Payment Entry", r.message);
				}
			},
		});
	});
}
