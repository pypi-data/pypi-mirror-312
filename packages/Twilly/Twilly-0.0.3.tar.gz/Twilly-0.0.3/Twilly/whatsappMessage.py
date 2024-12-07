from twilio.rest import Client
from django.conf import settings
from decimal import Decimal

def send_confirmation_message(property_item):

    price = property_item.price
    earning = (Decimal(price) * Decimal(0.05)) + 5

    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    # Send WhatsApp message to admin
    to_whatsapp_number = 'whatsapp:+353894828263'
    message = client.messages.create(
        body=f"Admin! A property was sold, and your earning is ${earning}",
        from_='whatsapp:+14155238886',
        to=to_whatsapp_number
    )

    return message.sid
