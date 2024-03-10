import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from typing import List
from magento import Client  # Ensure this is the correct import for your Magento API package
import magento


def get_shipping_address_for_invoice(latest_invoice):
    """
    Retrieve shipping address information for a specific invoice ID.

    :param invoice_id: The ID of the invoice to retrieve shipping address for.
    :return: A dictionary containing shipping address information.
    """
    # Fetch the invoice by its ID
    invoice = api.invoices.by_id(latest_invoice).execute()

    if not invoice:
        print(f"No invoice found with ID {latest_invoice}")
        return {}

    # Assuming the Invoice model has a way to access the associated order
    # The specific attribute/method to access the order may vary
    order = invoice.order

    if not order:
        print(f"No order associated with invoice ID {latest_invoice}")
        return {}

    # Assuming the Order model contains shipping address information
    # Adjust the attributes according to your actual Order model
    shipping_address = {
        "name": order.shipping_address.name,
        "street": order.shipping_address.street,
        "city": order.shipping_address.city,
        "region": order.shipping_address.region,
        "country": order.shipping_address.country,
        "postal_code": order.shipping_address.postal_code,
    }

    return shipping_address



# Suppress only the single InsecureRequestWarning from urllib3 needed
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Patch 'requests' to skip SSL verification
original_request = requests.Session.request  # Backup original request method


def patched_request(session, method, url, **kwargs):
    kwargs['verify'] = False  # Disable SSL verification
    return original_request(session, method, url, **kwargs)


requests.Session.request = patched_request  # Apply our patch to 'requests'

# Importing your magento package after patching 'requests'
import magento

# Authentication setup
domain = 'https://www.amstelbooks.com/'  # Your Magento instance
username = 'img'  # Replace with your actual username
password = 'maisli33sasdad'  # Replace with your actual password

# Setting up environment variables for convenience (optional)
os.environ['MAGENTO_DOMAIN'] = domain
os.environ['MAGENTO_USERNAME'] = username
os.environ['MAGENTO_PASSWORD'] = password

# Initialize the Magento API client
api = magento.get_api(domain=domain, username=username, password=password)


invoice_search = api.invoices

invoice_search.add_criteria(field='entity_id', value=True, condition='notnull')

# Execute the search to retrieve invoices with the specified criteria
invoices = invoice_search.execute()

# Assuming the returned 'invoices' is a list of Invoice model objects, and each has a 'created_at' attribute
# Sort the invoices by the 'created_at' attribute in descending order to find the latest
sorted_invoices = sorted(invoices, key=lambda invoice: invoice.created_at, reverse=True) if invoices else []

# The first invoice in the sorted list is the latest
latest_invoice = sorted_invoices[0] if sorted_invoices else None

if latest_invoice:
    # Access the properties of the latest invoice as needed
    print(f"Latest Invoice ID: {latest_invoice.id}")
    print(f"Created At: {latest_invoice.created_at}")
    # Continue accessing other necessary properties...
else:
    print("No invoices found.")

latest_invoice = latest_invoice.id
print (latest_invoice)

shipping_address = get_shipping_address_for_invoice(latest_invoice)

if shipping_address:
    print("Shipping Address Information:")
    for key, value in shipping_address.items():
        print(f"{key.title()}: {value}")
else:
    print("Shipping address information could not be retrieved.")