import os
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from magento import Client
from iso import country_id_to_name_fr
import logging
from datetime import datetime

# Configuration section
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
LOG_FILE = os.path.join(LOG_DIR, f'get_label_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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
    try:
        invoice = api.invoices.by_id(invoice_id)

        if not invoice:
            logging.error(f"No invoice found with ID {invoice_id}")
            return {}

        order = invoice.order

        if not order:
            logging.error(f"No order associated with invoice ID {invoice_id}")
            return {}

        shipping_address = order.shipping_address

        if not shipping_address:
            logging.error(f"No shipping address found for order associated with invoice ID {invoice_id}")
            return {}

        iso_code = shipping_address.get("country_id", "")
        country_name_fr = country_id_to_name_fr.get(iso_code, "Pays inconnu")

        shipping_address_info = {
            "name": shipping_address.get("firstname", "") + " " + shipping_address.get("lastname", ""),
            "street": " ".join(shipping_address.get("street", [])),
            "city": shipping_address.get("city", ""),
            "postal_code": shipping_address.get("postcode", ""),
            "country": country_name_fr,
            "phone": shipping_address.get("telephone", ""),
        }

        return shipping_address_info
    except Exception as e:
        logging.error(f"Error retrieving shipping address for invoice ID {invoice_id}: {str(e)}", exc_info=True)
        return {}

# Main script execution starts here
setup_ssl_patch()

# Authentication setup
domain = 'https://www.amstelbooks.com/'
username = 'img'
password = 'maisli33sasdad'

try:
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
        latest_invoice_id = latest_invoice.id
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

            with open(file_path, 'w') as file:
                json.dump([shipping_address], file, ensure_ascii=False, indent=4)

            logging.info(f"Shipping address information saved to {file_path}")
            print(f"Shipping address information saved to {file_path}")
        else:
            logging.error("Shipping address information could not be retrieved.")
            print("Shipping address information could not be retrieved.")
    else:
        logging.error("No invoices found.")
        print("No invoices found.")
except Exception as e:
    logging.error(f"Error during main script execution: {str(e)}", exc_info=True)
    print("An error occurred during script execution. Check the log file for details.")
