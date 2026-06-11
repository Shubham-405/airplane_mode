# Copyright (c) 2026, Shubham and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import random


class AirplaneTicket(Document):

    def validate(self):

        # Remove duplicate add-ons
        items = []
        unique_addons = []

        for addon in self.add_ons:
            if addon.item not in items:
                items.append(addon.item)
                unique_addons.append(addon)

        self.set("add_ons", unique_addons)

        # Calculate total amount
        total_addon = 0

        for addon in self.add_ons:
            total_addon += addon.amount

        self.total_amount = self.flight_price + total_addon

        # Check airplane capacity
        airplane = frappe.db.get_value(
            "Airplane Flight",
            self.flight,
            "airplane"
        )

        capacity = frappe.db.get_value(
            "Airplane",
            airplane,
            "capacity"
        )

        booked_tickets = frappe.db.count(
            "Airplane Ticket",
            {
                "flight": self.flight
            }
        )

        if booked_tickets >= capacity:
            frappe.throw("Flight is fully booked")

    def before_insert(self):

        number = random.randint(1, 99)

        alphabet = random.choice(
            ["A", "B", "C", "D", "E"]
        )

        self.seat = f"{number}{alphabet}"

    def before_submit(self):

        if self.status != "Boarded":
            frappe.throw("Passenger is not boarded")