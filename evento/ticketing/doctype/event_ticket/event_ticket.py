# Copyright (c) 2025, sabbir.kuasha@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EventTicket(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		attendee_name: DF.Data
		booking: DF.Link
		event: DF.Link
		qr_code: DF.AttachImage | None
		ticket_type: DF.Link
	# end: auto-generated types

	
	def after_insert(self):
		self.generate_qr_code()
	
	def generate_qr_code(self):
		import qrcode
		import io

		img = qrcode.make(self.name)
		img_bytes = io.BytesIO()
		img.save(img_bytes, format='PNG')
		file_content = img_bytes.getvalue()

		qr_code_file = frappe.get_doc({
			"doctype": "File",
			"content": file_content,
			"attached_to_doctype": "Event Ticket",
			"attached_to_name": self.name,
			"attached_to_field": "qr_code",
			"file_name": f"ticket-qr-code-{self.name}.png"
		}).save()

		self.qr_code = qr_code_file.file_url
		self.save()
