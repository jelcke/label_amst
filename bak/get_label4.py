import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from typing import List
from magento import Client  # Ensure this is the correct import for your Magento API package
import magento

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
