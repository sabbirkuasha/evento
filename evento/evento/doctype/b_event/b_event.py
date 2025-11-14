# Copyright (c) 2025, sabbir.kuasha@gmail.com and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class BEvent(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from evento.evento.doctype.schedule_item.schedule_item import ScheduleItem
		from frappe.types import DF

		banner_image: DF.AttachImage | None
		end_date: DF.Date
		end_time: DF.Time | None
		event_category: DF.Link
		event_description: DF.TextEditor | None
		event_flow: DF.Table[ScheduleItem]
		host: DF.Link
		is_published: DF.Check
		medium: DF.Literal["In-Person", "Online", "Hybrid"]
		short_description: DF.SmallText | None
		start_date: DF.Date
		start_time: DF.Time | None
		time_zone: DF.Autocomplete | None
		title: DF.Data
		venue: DF.Link
	# end: auto-generated types

	pass
