# Initialize the InvoiceSearch object through the client.invoices shortcut
invoice_search = api.invoices

# Add search criteria. This is a basic example that doesn't apply any filters,
# essentially asking for "all" invoices. Adjust according to your needs.
# For example, to filter invoices created after a specific date, you might use:
# invoice_search.add_criteria(field='created_at', value='2023-01-01', condition='gteq')
invoice_search.add_criteria(field='entity_id', value=True, condition='notnull')

# Execute the search to retrieve invoices with the specified criteria
invoices = invoice_search.execute()

# Continue with sorting and processing invoices as before...
