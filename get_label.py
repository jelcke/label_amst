import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from magento import Client
#from magento.client import Client
# Import the country_id_to_name_fr dictionary from the iso.py file
from iso import country_id_to_name_fr
import logging


logging.basicConfig(filename='logs/get_label.log', level=logging.ERROR)

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
        logging.error(f"No invoice found with ID {invoice_id}")
        return {}

    order = invoice.order

    if not order:
        print(f"No order associated with invoice ID {invoice_id}")
        logging.error(f"No order associated with invoice ID {invoice_id}")
        return {}

    shipping_address = order.shipping_address

    if not shipping_address:
        print(f"No shipping address found for order associated with invoice ID {invoice_id}")
        logging.error(f"No shipping address found for order associated with invoice ID {invoice_id}")
        return {}

    # Convert the country ID to the full country name in French
    iso_code = shipping_address.get("country_id", "")
    country_name_fr = country_id_to_name_fr.get(iso_code, "Pays inconnu")  # Fallback to "Pays inconnu" if not found


    # Correctly access dictionary values using keys
    shipping_address_info = {
        "name": shipping_address.get("firstname", "") + " " + shipping_address.get("lastname", ""),  # Combining first and last name
        "street": " ".join(shipping_address.get("street", [])),  # 'street' might be a list
        "city": shipping_address.get("city", ""),
        "postal_code": shipping_address.get("postcode", ""), 
        "country": country_name_fr,  # Magento often uses 'country_id' for country codes
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
    logging.info(f"Latest Invoice ID: {latest_invoice.id}")
    logging.info(f"Created At: {latest_invoice.created_at}")

    # Fetch shipping address for the latest invoice
#latest_invoice_id = latest_invoice.id -1  # get one invoice before
latest_invoice_id = latest_invoice.id    # Assuming latest_invoice is an invoice object and has an id attribute
shipping_address = get_shipping_address_for_invoice(api, latest_invoice_id)

if shipping_address:
    print("Shipping Address Information:")
    for key, value in shipping_address.items():
        print(f"{key.title()}: {value}")

    # Save to file called shipping_address{latest_invoice_id}.json in the json directory
    directory = '/home/jelcke/dev/prod/label_amst/json'
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, f'shipping_address{latest_invoice_id}.json')
    import json  # Make sure to import the json module at the beginning of your script

    shipping_addresses = [shipping_address]  # Make it a list containing your dictionary
    # Inside your if statement where you check if shipping_address exists
    with open(file_path, 'w') as file:
        json.dump(shipping_addresses, file, ensure_ascii=False, indent=4)

        print(f"Shipping address information saved to {file_path}")

else:
    print("Shipping address information could not be retrieved.")
