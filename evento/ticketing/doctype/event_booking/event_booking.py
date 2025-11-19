# Copyright (c) 2025, sabbir.kuasha@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EventBooking(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from evento.ticketing.doctype.event_booking_attendee.event_booking_attendee import EventBookingAttendee
		from frappe.types import DF

		amended_from: DF.Link | None
		currency: DF.Link | None
		event: DF.Link
		event_attendees: DF.Table[EventBookingAttendee]
		total_amount: DF.Currency
		user: DF.Link
	# end: auto-generated types

	def validate(self):
		self.set_total_amount()
		if not self.currency and self.event:
			self.set_currency_from_event()

	def set_total_amount(self):
		self.total_amount = 0
		for attendee in self.event_attendees:
			self.total_amount += attendee.price
		
	def set_currency_from_event(self):
		self.currency = frappe.db.get_value("Event", self.event, "currency")

	def on_submit(self):
		self.generate_ticket()
		frappe.msgprint(f"Tickets generated for booking {self.name}")

	def generate_ticket(self):
		for attendee in self.event_attendees:
			ticket = frappe.new_doc("Event Ticket")
			ticket.event = self.event
			ticket.booking = self.name 
			ticket.ticket_type = attendee.ticket_type
			ticket.attendee_name = attendee.get("full_name")
			ticket.insert().submit()