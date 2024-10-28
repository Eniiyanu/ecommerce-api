# core/utils.py

import random
import string

def generate_sku():
    """Generate a random Store Keeping Unit number for a product."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
