# Copyright 2024
# Directory: yt-rag/app/data/default_documents.py

"""
Default documents for seeding the RAG knowledge base.
Contains sample policy and support information for demonstration.
"""

from typing import List, Dict

# Default documents for seeding
DEFAULT_DOCUMENTS: List[Dict[str, str]] = [
    {
        'chunk_id': 'policy_returns_v1',
        'source': 'https://help.example.com/return-policy',
        'text': '''Return Policy

You can return unworn items within 30 days of purchase with original receipt. Items must be in original condition with tags attached. 

IMPORTANT: Items over $200 require manual approval for returns. Please email support@company.com with your order details for items over $200.

Exceptions: Final sale items, customized products, and intimate apparel cannot be returned. Shoes must be unworn with original box.

Refunds will be processed to original payment method within 5-7 business days after we receive your return.'''
    },
    {
        'chunk_id': 'policy_shipping_v1',
        'source': 'https://help.example.com/shipping',
        'text': '''Shipping Information

Free standard shipping on orders over $50. Standard shipping takes 3-5 business days. Express shipping available for $9.99 (1-2 business days).

International shipping available to select countries. Shipping costs calculated at checkout based on destination and weight.

Orders placed before 2 PM EST ship same day. Weekend orders ship on the next business day.'''
    },
    {
        'chunk_id': 'sizing_guide_v1',
        'source': 'https://help.example.com/sizing',
        'text': '''Size Guide

Clothing sizes run true to size. Please refer to our size chart for measurements.

For shoes: If between sizes, we recommend sizing up for comfort. Athletic shoes may run small - consider sizing up half a size.

Exchanges for different sizes are free within 30 days. Use our online size guide tool for personalized recommendations.'''
    },
    {
        'chunk_id': 'support_contact_v1',
        'source': 'https://help.example.com/contact',
        'text': '''Customer Support

Contact us Monday-Friday 9 AM - 6 PM EST:
- Email: support@example.com
- Phone: 1-800-555-0123
- Live chat available on our website

For order issues, have your order number ready. Response time is typically within 24 hours for email inquiries.

You can also track your order status online using your order number and email address.'''
    }
]
