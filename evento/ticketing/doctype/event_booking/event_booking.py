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
		"""Calculate total amount from attendee prices."""
		self.total_amount = 0
		for attendee in self.event_attendees:
			self.total_amount += attendee.price
		
	def set_currency_from_event(self):
		"""Set currency from the linked event."""
		# It's generally better to get currency from the parent event
		# to ensure consistency.
		self.currency = frappe.db.get_value("Event", self.event, "currency")

	def on_submit(self):
		self.generate_ticket()
		frappe.msgprint(f"Tickets generated for booking {self.name}")

	def on_cancel(self):
		self.cancel_tickets()

	def generate_ticket(self):
		for attendee in self.event_attendees:
			ticket = frappe.new_doc("Event Ticket")
			ticket.event = self.event
			ticket.booking = self.name 
			ticket.ticket_type = attendee.ticket_type
			ticket.attendee_name = attendee.get("full_name")
			# Use ignore_permissions as the permission is already checked on EventBooking submission
			ticket.save(ignore_permissions=True)
			# ticket.insert(ignore_permissions=True)
			# Submitting tickets one by one in a loop can be slow.
			# Consider if auto-submission is necessary or can be done in a background job.
			ticket.submit()

	def cancel_tickets(self):
		"""Cancel all tickets associated with this booking."""
		# Assuming the fieldname in 'Event Ticket' linking to 'Event Booking' is 'booking'
		ticket_names = frappe.get_all("Event Ticket", filters={"booking": self.name}, pluck="name")

		for name in ticket_names:
			ticket = frappe.get_doc("Event Ticket", name)
			if ticket.docstatus == 1: # Only cancel submitted tickets
				ticket.cancel()
		frappe.msgprint(f"Tickets for booking {self.name} have been cancelled.")