from twilio.rest import Client

class TwillioClient:

    def __init__(self):
        self.client = None

    def connect(self):
        account_sid = 'AC7ace3468f7e53936b2c49e16ad354814'
        auth_token = 'e5ef2d9cfd2925c66f662b9311d3f066'
        self.client = Client(account_sid, auth_token)

    def send_message(self, message):
        message = self.client.messages.create(
          from_='whatsapp:+14155238886',
          body=message,
          to='whatsapp:+94772608766' #'whatsapp:+94712986468' 'whatsapp:+6597778562' #
        )
        print(message.sid)