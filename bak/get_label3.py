from magento import Client  # Ensure this is the correct import for your Magento API package

# Initialize the Magento API client
client = Client(
    domain='https://www.amstelbooks.nl/',
    username = 'img',  # Replace with your actual username
    password = 'maisli33sasdad'  # Replace with your actual password
    # Add any other required parameters
)

# Assuming the InvoiceSearch object returned by client.invoices has a method to list invoices
# This is a placeholder; you'll need to replace `list_invoices` with the actual method name
invoices = client.invoices.list_invoices()

# Sort the invoices by a date field (e.g., 'created_at') in descending order to get the latest invoice first
# Replace 'created_at' with the actual field name used by the API for the invoice creation date
sorted_invoices = sorted(invoices, key=lambda x: x['created_at'], reverse=True)

# The first invoice in the sorted list is the latest
latest_invoice = sorted_invoices[0] if sorted_invoices else None

if latest_invoice:
    print("Latest Invoice:", latest_invoice)
else:
    print("No invoices found.")