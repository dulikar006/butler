import json
import os

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


class TwillioClient:

    def __init__(self):
        self.root_number = 'whatsapp:+94768813566'
        self.client = None

    def connect(self):
        account_sid = os.environ['twillio_id']
        auth_token = os.environ['twillio_key']
        self.client = Client(account_sid, auth_token)

    def send_message(self, message, phone_number):
        try:
            message = self.client.messages.create(
                from_=self.root_number,
                body=message,
                to=f"whatsapp:+{phone_number}"
                # 'whatsapp:+94772608766' #'whatsapp:+94712986468' 'whatsapp:+6597778562' #
            )
            print(message.sid)
        except:
            print("Error sending whatsapp message")

    def send_template_message(self, name, hotel_name, sender, phone_number):
        try:
            message = self.client.messages.create(
                content_sid="HX3f34b459bef9b83cf3ee6cd66b4b0009",
                to=f"whatsapp:+{phone_number}",
                from_=self.root_number,
                content_variables=json.dumps({"1": name, "2": hotel_name, "3": sender}),
                # messaging_service_sid="MGXXXXXXXX",
            )

            print(message.body)
        except Exception as err:
            print(f"Error sending whatsapp message  - {err}")

    def send_confirmation_message(self, agent_message, phone_number):
        try:
            message = self.client.messages.create(
                content_sid="HX4e11c430890b40e3199c62142ada753a",  # Replace with your approved template SID
                to=f"whatsapp:+{phone_number}",  # Ensure phone number is correct with country code
                from_=self.root_number,
                content_variables=json.dumps({
                    "8": agent_message,  # Replace '8' with actual template placeholder
                    "5": "123c",  # Replace '5' and '7' with actual template placeholders
                    "7": "123i"
                })
            )

            print(f"Message SID: {message.sid}")
            print(f"Message Status: {message.status}")  # Add message status tracking
            # return message.sid

        except TwilioRestException as e:
            print(f"Twilio error occurred: {e}")
        except Exception as err:
            print(f"Error sending WhatsApp message: {err}")
