from typing import Dict, List
from dataclasses import dataclass
from datetime import timedelta

@dataclass
class InvoiceDefaults:
    """Default values for invoice generation."""
    currency: str = "USD"
    payment_days: int = 30
    tax_rates: List[float] = (10.0, 15.0, 20.0)
    min_items: int = 1
    max_items: int = 5
    min_item_quantity: int = 1
    max_item_quantity: int = 10
    min_item_price: float = 10.0
    max_item_price: float = 1000.0

@dataclass
class OutputConfig:
    """Configuration for output files."""
    default_output_dir: str = "invoices"
    pdf_filename_template: str = "invoice_{number}.pdf"
    date_format: str = "%Y-%m-%d"

@dataclass
class LocaleConfig:
    """Configuration for localization."""
    default_locale: str = "en_US"
    available_locales: List[str] = ("en_US", "en_GB", "fr_FR", "de_DE", "es_ES")
    date_format: str = "%Y-%m-%d"
    currency_format: Dict[str, Dict] = {
        "USD": {"symbol": "$", "position": "prefix"},
        "EUR": {"symbol": "€", "position": "suffix"},
        "GBP": {"symbol": "£", "position": "prefix"},
    }

class Config:
    """Main configuration class for FakeInvoiceGen."""
    
    def __init__(self):
        self.invoice = InvoiceDefaults()
        self.output = OutputConfig()
        self.locale = LocaleConfig()
        
    @property
    def payment_term(self) -> timedelta:
        """Get payment term as timedelta."""
        return timedelta(days=self.invoice.payment_days)
    
    def get_currency_format(self, currency_code: str) -> Dict:
        """
        Get currency formatting rules for given currency code.
        
        Args:
            currency_code (str): Currency code (e.g., 'USD', 'EUR')
            
        Returns:
            Dict: Currency formatting configuration
        """
        return self.locale.currency_format.get(
            currency_code,
            {"symbol": currency_code, "position": "prefix"}
        )
    
    def is_supported_locale(self, locale: str) -> bool:
        """
        Check if locale is supported.
        
        Args:
            locale (str): Locale code to check
            
        Returns:
            bool: True if locale is supported
        """
        return locale in self.locale.available_locales

# Global configuration instance
config = Config()

# Additional configuration constants
SUPPORTED_CURRENCIES = ['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'JPY']
SUPPORTED_PAYMENT_TERMS = [7, 14, 30, 45, 60, 90]

# Template configurations
INVOICE_TEMPLATES = {
    'default': {
        'font': 'DejaVu Sans',
        'font_size': 10,
        'page_size': 'A4',
        'margin_top': 3,
        'margin_right': 3,
        'margin_bottom': 3,
        'margin_left': 3,
    },
    'minimal': {
        'font': 'DejaVu Sans',
        'font_size': 9,
        'page_size': 'A4',
        'margin_top': 2,
        'margin_right': 2,
        'margin_bottom': 2,
        'margin_left': 2,
    },
    'professional': {
        'font': 'DejaVu Serif',
        'font_size': 11,
        'page_size': 'A4',
        'margin_top': 4,
        'margin_right': 3,
        'margin_bottom': 4,
        'margin_left': 3,
    }
}

# PDF generation settings
PDF_SETTINGS = {
    'compression': True,
    'title_max_length': 50,
    'description_max_length': 100,
    'item_description_max_length': 80,
}

# Validation settings
VALIDATION_RULES = {
    'min_total_amount': 0.01,
    'max_total_amount': 1000000.00,
    'max_items_per_invoice': 100,
    'max_quantity_per_item': 1000,
    'allowed_tax_rates': [0, 5, 10, 15, 20, 25],
}

def get_template_config(template_name: str = 'default') -> Dict:
    """
    Get configuration for specified template.
    
    Args:
        template_name (str): Name of the template to use
        
    Returns:
        Dict: Template configuration
    """
    return INVOICE_TEMPLATES.get(template_name, INVOICE_TEMPLATES['default'])

def validate_currency(currency: str) -> bool:
    """
    Validate if currency is supported.
    
    Args:
        currency (str): Currency code to validate
        
    Returns:
        bool: True if currency is supported
    """
    return currency in SUPPORTED_CURRENCIES

def validate_payment_term(days: int) -> bool:
    """
    Validate if payment term is supported.
    
    Args:
        days (int): Number of days for payment term
        
    Returns:
        bool: True if payment term is supported
    """
    return days in SUPPORTED_PAYMENT_TERMS

# Error messages
ERROR_MESSAGES = {
    'invalid_currency': 'Invalid currency code. Supported currencies are: {currencies}',
    'invalid_payment_term': 'Invalid payment term. Supported terms are: {terms} days',
    'invalid_template': 'Invalid template name. Available templates are: {templates}',
    'invalid_locale': 'Invalid locale. Supported locales are: {locales}',
    'invalid_amount': 'Total amount must be between {min_amount} and {max_amount}',
    'too_many_items': 'Number of items exceeds maximum limit of {max_items}',
}