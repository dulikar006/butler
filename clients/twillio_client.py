import json
import os

from twilio.rest import Client

class TwillioClient:

    def __init__(self):
        self.client = None

    def connect(self):
        account_sid = os.environ['twillio_id']
        auth_token = os.environ['twillio_key']
        self.client = Client(account_sid, auth_token)

    def send_message(self, message, phone_number):
        try:
            message = self.client.messages.create(
              from_='whatsapp:+94768813566',
              body=message,
              to=f"whatsapp:+{phone_number}" #'whatsapp:+94772608766' #'whatsapp:+94712986468' 'whatsapp:+6597778562' #
            )
            print(message.sid)
        except:
            print("Error sending whatsapp message")


    def send_template_message(self, name, hotel_name, sender, phone_number):
        try:
            message = self.client.messages.create(
                content_sid="HX3f34b459bef9b83cf3ee6cd66b4b0009",
                to=f"whatsapp:+{phone_number}",
                from_='whatsapp:+94768813566',
                content_variables=json.dumps({"1": name, "2": hotel_name, "3": sender}),
                # messaging_service_sid="MGXXXXXXXX",
            )

            print(message.body)
        except Exception as err:
            print(f"Error sending whatsapp message  - {err}")