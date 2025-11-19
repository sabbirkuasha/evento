# Copyright (c) 2025, sabbir.kuasha@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import random_string
from frappe.website.website_generator import WebsiteGenerator


class FootballRegistration(WebsiteGenerator):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		area: DF.Literal["Dhaka", "Bogura"]
		name1: DF.Data | None
		phone: DF.Data | None
		published: DF.Check
		qr_code: DF.AttachImage | None
		route: DF.Data | None
	# end: auto-generated types

	def make_route(self):
		from_title =  random_string(16)
		if self.meta.route:
			return self.meta.route + "/" + from_title
		else:
			return from_title

	def after_insert(self):
		self.generate_qr_code()

	def generate_qr_code(self):
		import io

		import qrcode

		# Combine all data
		qr_code = f"Name: {self.name1}, Phone: {self.phone}, Area: {self.area}"

		# Create QR code
		img = qrcode.make(qr_code)
		img_bytes = io.BytesIO()
		img.save(img_bytes, format='PNG')
		file_content = img_bytes.getvalue()

		# save as a file document
		qr_code_file = frappe.get_doc({
			"doctype": "File",
			"content": file_content,
			"attached_to_doctype": self.doctype,
			"attached_to_name": self.name1,
			"attached_to_field": "qr_code",
			"file_name": f"registration-qr-code-{self.name1}.png",
			"is_private": 0
			}).save()

		self.db_set("qr_code", qr_code_file.file_url)

