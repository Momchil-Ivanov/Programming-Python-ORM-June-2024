import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import VideoGame, Invoice, BillingInfo

# Create BillingInfo instances with real addresses
# billing_info_1 = BillingInfo.objects.create(address="456 Oak Lane, Boston, MA 02108")
#
# billing_info_2 = BillingInfo.objects.create(address="789 Maple Avenue, San Francisco, CA 94101")
#
# billing_info_3 = BillingInfo.objects.create(address="101 Pine Street, New York, NY 10001")
#
# # Create Invoice instances with related BillingInfo
# invoice_1 = Invoice.objects.create(invoice_number="INV007", billing_info=billing_info_1)
#
# invoice_2 = Invoice.objects.create(invoice_number="INV002", billing_info=billing_info_2)
# invoice_3 = Invoice.objects.create(invoice_number="INV004", billing_info=billing_info_3)
#
# # Get invoices starting with a specific prefix
# invoices_with_prefix = Invoice.get_invoices_with_prefix("INV")
#
# for invoice in invoices_with_prefix:
#     print(f"Invoice Number with prefix INV: {invoice.invoice_number}")
#
# # Get invoices sorted by invoice number
# invoices_sorted = Invoice.get_invoices_sorted_by_number()
#
# for invoice in invoices_sorted:
#     print(f"Invoice Number: {invoice.invoice_number}")
#
# # Get an invoice by a specific invoice number along with its related billing info
# invoice = Invoice.get_invoice_with_billing_info("INV002")
# print(f"Invoice Number: {invoice.invoice_number}")
# print(f"Billing Info: {invoice.billing_info.address}")
