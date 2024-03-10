import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning from urllib3 needed
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Patch 'requests' to skip SSL verification
original_request = requests.Session.request  # Backup original request method


def patched_request(session, method, url, **kwargs):
    kwargs['verify'] = False  # Disable SSL verification
    return original_request(session, method, url, **kwargs)


requests.Session.request = patched_request  # Apply our patch to 'requests'

import magento  # Ensure to import 'magento' after patching 'requests'

# Your existing code starts here
domain = 'https://www.amstelbooks.com/'  # Your Magento instance
username = 'img'  # Your API username
password = 'maisli33sasdad'  # Your API password

os.environ['MAGENTO_DOMAIN'] = domain
os.environ['MAGENTO_USERNAME'] = username
os.environ['MAGENTO_PASSWORD'] = password

api = magento.get_api(domain=domain, username=username, password=password)

try:
    # Attempt to list invoices directly
    invoices = api.invoices.list()
except AttributeError:
    print("The InvoiceSearch object does not have a 'list' method. Please check the correct method to fetch invoices.")
    invoices = []

# If the invoices are not automatically sorted by date, you may need to sort them manually
# Replace 'created_at' with the actual attribute used by your Invoice objects for the creation date
sorted_invoices = sorted(invoices, key=lambda x: x.created_at, reverse=True)

# The first invoice in the sorted list is the latest
latest_invoice = sorted_invoices[0] if sorted_invoices else None

if latest_invoice:
    # Now you can access the latest invoice's properties using the methods and properties of the Invoice class
    print(f"Latest Invoice ID: {latest_invoice.id}")
    print(f"Invoice Number: {latest_invoice.number}")
    print(f"Order Associated: {latest_invoice.order}")
    print(f"Customer: {latest_invoice.customer}")

    # Example of iterating over the items in the latest invoice
    for item in latest_invoice.items:
        print(f"Item SKU: {item.sku}, Quantity: {item.quantity}")
else:
    print("No invoices found.")
