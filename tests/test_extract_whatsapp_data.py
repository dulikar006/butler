import unittest

from transformers.process_input_transformer import extract_whatsapp_data


# Unit test class
class TestExtractWhatsappData(unittest.TestCase):

    def test_extract_whatsapp_data(self):
        input_data = {
            'MediaContentType0': 'image/jpeg',
            'SmsMessageSid': 'MMff487f182469b2cbbf01866c5970dcee',
            'NumMedia': '1',
            'ProfileName': 'Dulika Ranasinghe',
            'MessageType': 'image',
            'SmsSid': 'MMff487f182469b2cbbf01866c5970dcee',
            'WaId': '94712986468',
            'SmsStatus': 'received',
            'Body': 'my medical',
            'To': 'whatsapp:+94768813566',
            'NumSegments': '1',
            'ReferralNumMedia': '0',
            'MessageSid': 'MMff487f182469b2cbbf01866c5970dcee',
            'AccountSid': 'AC7ace3468f7e53936b2c49e16ad354814',
            'From': 'whatsapp:+94712986468',
            'MediaUrl0': 'https://api.twilio.com/2010-04-01/Accounts/AC7ace3468f7e53936b2c49e16ad354814/Messages/MMff487f182469b2cbbf01866c5970dcee/Media/MEafacf1f30173b860e0e71ca8c3e8b5fe',
            'ApiVersion': '2010-04-01'
        }

        expected_output = {
            'media_content_type': 'image/jpeg',
            'sms_message_sid': 'MMff487f182469b2cbbf01866c5970dcee',
            'num_media': '1',
            'profile_name': 'Dulika Ranasinghe',
            'message_type': 'image',
            'sms_sid': 'MMff487f182469b2cbbf01866c5970dcee',
            'wa_id': '94712986468',
            'sms_status': 'received',
            'body': 'my medical',
            'to': 'whatsapp:+94768813566',
            'num_segments': '1',
            'referral_num_media': '0',
            'message_sid': 'MMff487f182469b2cbbf01866c5970dcee',
            'account_sid': 'AC7ace3468f7e53936b2c49e16ad354814',
            'from_whatsapp': 'whatsapp:+94712986468',
            'media_url': 'https://api.twilio.com/2010-04-01/Accounts/AC7ace3468f7e53936b2c49e16ad354814/Messages/MMff487f182469b2cbbf01866c5970dcee/Media/MEafacf1f30173b860e0e71ca8c3e8b5fe',
            'api_version': '2010-04-01'
        }

        # Call the function with the test data
        result = extract_whatsapp_data(input_data)

        # Assert that the result matches the expected output
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
