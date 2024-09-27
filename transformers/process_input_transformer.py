import json

from clients.openai_client import call_openai
from clients.twillio_client import TwillioClient
from database.redis_cache_manager import RedisCacheManager
from helpers.load_response import generate_response
from utilities.prompts import action_identification




def extract_whatsapp_data(data: dict):
    sms_message_sid = data.get('SmsMessageSid')
    profile_name = data.get('ProfileName')
    message_type = data.get('MessageType')
    sms_sid = data.get('SmsSid')
    wa_id = data.get('WaId')
    sms_status = data.get('SmsStatus')
    body = data.get('Body')
    to = data.get('To')
    num_segments = data.get('NumSegments')
    referral_num_media = data.get('ReferralNumMedia')
    message_sid = data.get('MessageSid')
    account_sid = data.get('AccountSid')
    from_whatsapp = data.get('From')
    api_version = data.get('ApiVersion')
    attachment_description = None

    if data.get('NumMedia') != '0' and data.get('MediaContentType0'):
        media_content_type = data.get('MediaContentType0')
        num_media = data.get('NumMedia')
        media_url = data.get('MediaUrl0')
        attachment_description = process_attachment_message(media_content_type, num_media, media_url, body)

    chat_history = get_chat_history(account_sid)

    action, criteria = identify_action(chat_history, body)

    if action == 'True':
        response = f'''I apologize, but I’m unable to assist with your request on {criteria} at the moment. However, I’ve informed my manager, and they will be in touch with you shortly. Please feel free to let me know if there’s anything else I can assist you with in the meantime.'''
        tc = TwillioClient()
        tc.connect()
        tc.send_message(f"Hi Mr.Malaka, Our guest at room number 38 is requesting an action on {criteria}. Can you please do the needful. \n - Shalini, Careline Agent.")

    else:
        response = generate_response(body, chat_history=chat_history)

    update_history(account_sid, body, response)

    response += "\n - Shalini, Careline Agent."

    return response

    # return {
    #     'sms_message_sid': sms_message_sid,
    #     'profile_name': profile_name,
    #     'message_type': message_type,
    #     'sms_sid': sms_sid,
    #     'wa_id': wa_id,
    #     'sms_status': sms_status,
    #     'body': body,
    #     'to': to,
    #     'num_segments': num_segments,
    #     'referral_num_media': referral_num_media,
    #     'message_sid': message_sid,
    #     'account_sid': account_sid,
    #     'from_whatsapp': from_whatsapp,
    #     'api_version': api_version,
    #     'attachment_description': attachment_description,
    #     'chat_history': chat_history
    # }


# TO-DO
def process_attachment_message(media_content_type, num_media, media_url, body):
    pass


def get_chat_history(user_id):
    rcm = RedisCacheManager()
    rcm.connect()
    history = rcm.get_conversation_history(user_id)
    if isinstance(history, list) and len(history)>0:
        return history
    print('error loading cache history')
    return []

def update_history(user_id, question, response):
    rcm = RedisCacheManager()
    rcm.connect()
    rcm.store_conversation(user_id, 'user', question, expire_time=3600)
    rcm.store_conversation(user_id, 'agent', response, expire_time=3600)

def identify_action(chat_history, question):
    json_string = call_openai(action_identification, {"chat_history": chat_history, "question": question})
    first_brace_index = json_string.find('{')
    last_brace_index = json_string.rfind('}')
    extracted_json = json_string[first_brace_index:last_brace_index + 1]
    extracted_json = extracted_json.replace("'", '"')
    result_dict = json.loads(extracted_json)
    action = result_dict.get('result').get('action')
    criteria = result_dict.get('result').get('criteria')
    return action, criteria
