from twilio.rest import Client

class TwillioClient:

    def __init__(self):
        self.client = None

    def connect(self):
        account_sid = 'AC7ace3468f7e53936b2c49e16ad354814'
        auth_token = '9e6e8059b3a62f7b5ad6d18cdacb7094'
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