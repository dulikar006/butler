import os

from twilio.rest import Client

class TwillioClient:

    def __init__(self):
        self.client = None

    def connect(self):
        account_sid = os.environ['twillio_id']
        auth_token = os.environ['twillio_key']
        self.client = Client(account_sid, auth_token)

    def send_message(self, message):
        try:
            message = self.client.messages.create(
              from_='whatsapp:+14155238886',
              body=message,
              to="whatsapp:+94712986468" #'whatsapp:+94772608766' #'whatsapp:+94712986468' 'whatsapp:+6597778562' #
            )
            print(message.sid)
        except:
            print("Error sending whatsapp message")