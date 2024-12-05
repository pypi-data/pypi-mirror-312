import os
from faker import Faker
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
from typing import List, Optional, Dict

class InvoiceGenerator:
    """
    A class to generate fake invoices using Faker and InvoiceGenerator libraries.
    """
    
    def __init__(self):
        """Initialize the InvoiceGenerator."""
        # Set English as default language
        os.environ["INVOICE_LANG"] = "en"
        self.fake = Faker()

    def generate_invoice(self, 
                        output_path: str = "invoice.pdf",
                        custom_data: Optional[Dict] = None) -> str:
        """
        Generate a single invoice.

        Args:
            output_path (str): Path where to save the invoice PDF
            custom_data (dict, optional): Custom invoice data

        Returns:
            str: Path to the generated invoice PDF
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        # Generate or use custom data
        if custom_data is None:
            custom_data = {}

        # Create client
        client_name = custom_data.get('client_name', self.fake.company())
        client = Client(client_name)

        # Create provider
        provider_name = custom_data.get('provider_name', self.fake.company())
        bank_account = custom_data.get('bank_account', self.fake.iban())
        bank_code = custom_data.get('bank_code', self.fake.swift())
        provider = Provider(provider_name, bank_account=bank_account, bank_code=bank_code)

        # Create creator
        creator_name = custom_data.get('creator_name', self.fake.name())
        creator = Creator(creator_name)

        # Create invoice
        invoice = Invoice(client, provider, creator)
        invoice.currency_locale = custom_data.get('currency_locale', 'en_US.UTF-8')

        # Add items
        items = custom_data.get('items', [
            {'qty': 32, 'price': 600, 'description': "Item 1", 'tax': 21},
            {'qty': 60, 'price': 50, 'description': "Item 2", 'tax': 21},
            {'qty': 50, 'price': 60, 'description': "Item 3", 'tax': 0},
            {'qty': 5, 'price': 600, 'description': "Item 4", 'tax': 15}
        ])

        for item in items:
            invoice.add_item(Item(
                count=item.get('qty'),
                price=item.get('price'),
                description=item.get('description', self.fake.bs()),
                tax=item.get('tax', 21)
            ))

        # Generate PDF
        pdf = SimpleInvoice(invoice)
        pdf.gen(output_path, generate_qr_code=True)

        return output_path

    def generate_invoices(self, 
                         count: int = 1,
                         output_dir: str = "invoices") -> List[str]:
        """
        Generate multiple invoices.

        Args:
            count (int): Number of invoices to generate
            output_dir (str): Directory to save the invoices

        Returns:
            List[str]: List of paths to generated invoice PDFs
        """
        paths = []
        os.makedirs(output_dir, exist_ok=True)

        for i in range(count):
            output_path = os.path.join(output_dir, f"invoice_{i+1}.pdf")
            path = self.generate_invoice(output_path=output_path)
            paths.append(path)

        return paths