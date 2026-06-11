import frappe

def send_rent_reminders():
    frappe.logger().info("Rent Reminder Executed")