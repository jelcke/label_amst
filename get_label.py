import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from magento import Client

# Function to disable SSL verification warnings and patch requests for all instances
def setup_ssl_patch():
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    original_request = requests.Session.request

    def patched_request(session, method, url, **kwargs):
        kwargs['verify'] = False  # Disable SSL verification
        return original_request(session, method, url, **kwargs)

    requests.Session.request = patched_request

# Function to retrieve shipping address for a given invoice
def get_shipping_address_for_invoice(api, invoice_id):
    # Fetch the invoice by its ID
    invoice = api.invoices.by_id(invoice_id)

    if not invoice:
        print(f"No invoice found with ID {invoice_id}")
        return {}

    order = invoice.order

    if not order:
        print(f"No order associated with invoice ID {invoice_id}")
        return {}

    shipping_address = order.shipping_address

    if not shipping_address:
        print(f"No shipping address found for order associated with invoice ID {invoice_id}")
        return {}

    # Correctly access dictionary values using keys
    shipping_address_info = {
        "name": shipping_address.get("firstname", "") + " " + shipping_address.get("lastname", ""),  # Combining first and last name
        "street": " ".join(shipping_address.get("street", [])),  # 'street' might be a list
        "city": shipping_address.get("city", ""),
        "region": shipping_address.get("region", ""),  # Sometimes 'region' might be a dictionary with 'region' as a key inside it
        "country": shipping_address.get("country_id", ""),  # Magento often uses 'country_id' for country codes
        "postal_code": shipping_address.get("postcode", ""), 
        "phone": shipping_address.get("telephone", ""),  # Added line for phone number
    }


    return shipping_address_info


# Main script execution starts here
setup_ssl_patch()

# Authentication setup
domain = 'https://www.amstelbooks.com/'
username = 'img'
password = 'maisli33sasdad'

# Initialize the Magento API client
api = Client(domain=domain, username=username, password=password)

# Fetch and sort invoices to find the latest one
invoice_search = api.invoices
invoice_search.add_criteria(field='entity_id', value=True, condition='notnull')
invoices = invoice_search.execute()
sorted_invoices = sorted(invoices, key=lambda invoice: invoice.created_at, reverse=True) if invoices else []

latest_invoice = sorted_invoices[0] if sorted_invoices else None

if latest_invoice:
    print(f"Latest Invoice ID: {latest_invoice.id}")
    print(f"Created At: {latest_invoice.created_at}")

    # Fetch shipping address for the latest invoice
latest_invoice_id = latest_invoice.id  # Assuming latest_invoice is an invoice object and has an id attribute
shipping_address = get_shipping_address_for_invoice(api, latest_invoice_id)

if shipping_address:
    print("Shipping Address Information:")
    for key, value in shipping_address.items():
        print(f"{key.title()}: {value}")
else:
    print("Shipping address information could not be retrieved.")
