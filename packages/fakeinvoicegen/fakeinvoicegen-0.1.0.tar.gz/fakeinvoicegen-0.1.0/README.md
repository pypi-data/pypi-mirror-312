# FakeInvoiceGen

A Python package that generates fake invoices using Faker and InvoiceGenerator libraries.

## Features

- Generate any number of random invoices with fake data
- Customize invoice data with your own inputs
- Easy to use API
- Configurable invoice templates

## Installation

```bash
pip install fakeinvoicegen
```

## Quick Start

```python
from fakeinvoicegen import InvoiceGenerator

# Generate 5 random invoices
generator = InvoiceGenerator()
generator.generate_invoices(count=5)

# Generate invoice with custom data
custom_data = {
    'client_name': 'John Doe',
    'amount': 1000.00,
    'due_date': '2024-12-31'
}
generator.generate_invoice(custom_data=custom_data)
```
