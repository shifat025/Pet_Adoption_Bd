import paypalrestsdk
from django.conf import settings


# Configure PayPal
paypalrestsdk.configure({
    "mode": "sandbox",  # or "live"
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

def create_paypal_payment(price, description, return_url, cancel_url):
    """
    Creates a PayPal payment for the given price and description.
    Returns the redirect URL if successful, otherwise returns None.
    """
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": return_url,
            "cancel_url": cancel_url
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": description,
                    "sku": description.lower().replace(" ", "_"),
                    "price": f"{price:.2f}",
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": f"{price:.2f}",
                "currency": "USD"
            },
            "description": description
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                return link.href
    return None
