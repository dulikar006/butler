import json

from clients.openai_client import call_openai
from clients.postgres_client import PostgresClient
from clients.twillio_client import TwillioClient
from database.redis_cache_manager import RedisCacheManager
from helpers.history_helpers import get_chat_history, update_history
from helpers.json_helper import convert_to_json
from helpers.load_response import generate_response
from transformers.order_creation_transformer import extract_whatsapp_data_for_order_creation
from utilities.prompts import action_identification, action_route, parameters_prompting


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

    '''check if the message is part of order creation process'''
    redis_manager = RedisCacheManager()
    redis_manager.connect()
    category = redis_manager.is_order_creation(account_sid)
    if isinstance(category, list) and len(category)>0:
        category = category[0]
        if category != 0 or "0" not in category:
            '''check if current question is about the booking or completely different, if different, ask still want to continue with the order'''
            response = extract_whatsapp_data_for_order_creation(profile_name, account_sid, category, body, chat_history)
            response += "\n - Shalini, Careline Agent."
            update_history(account_sid, body, response)
            return response

    action, criteria = identify_action(chat_history, body)

    if action == 'True':

        is_category, response = route_action(account_sid, chat_history, body, criteria)

        if is_category: #if identified action, respond to prompt required information
            update_history(account_sid, body, response)
            if isinstance(response, dict):
                response = f"Please provide these details to proceed with the order - {str(response)}"
            response += "\n - Shalini, Careline Agent."
            return response

        response = f'''I apologize, but I’m unable to assist with your request on {criteria} at the moment. However, I’ve informed my manager, and they will be in touch with you shortly. Please feel free to let me know if there’s anything else I can assist you with in the meantime.'''
        tc = TwillioClient()
        tc.connect()
        tc.send_message(f"Hi Mr.Malaka, Our guest at room number 38 is requesting an action on {criteria}. Can you please do the needful. \n - Shalini, Careline Agent.",
                        '94772608766')

    else:
        response = generate_response(body, chat_history=chat_history)

    update_history(account_sid, body, response)

    response += "\n - Shalini, Careline Agent."

    return response


# TO-DO
def process_attachment_message(media_content_type, num_media, media_url, body):
    pass




def identify_action(chat_history, question):
    json_string = call_openai(action_identification, {"chat_history": chat_history, "question": question})
    result_dict = convert_to_json(json_string)
    action = result_dict.get('action')
    criteria = result_dict.get('criteria')
    return action, criteria

def route_action(user_id, chat_history, question, criteria):

    pc = PostgresClient()
    pc.connect()
    actions_list = pc.fetch_all('select id, function, name, description from public.actions')

    output = ""
    for i, (order_id, function, order_name, order_desc) in enumerate(actions_list, 1):
        output += f"   - {function} - {order_name} - {order_desc} - action_id - {order_id}\n"

    json_string = call_openai(action_route, {"chat_history": chat_history, "question": question,
                                                      "criteria": criteria, "action_fields": output})
    result_dict = convert_to_json(json_string)
    action_id = int(result_dict.get('action_id'))
    if action_id == 0:
        return False, None

    sql = f'select distinct fields from public.actions where id = {action_id}'
    required_params = pc.fetch_one(sql)
    params_input = ""
    for item in required_params[0]:
        params_input += f"{item['detail']} (Example: {item['example']}, {item['mandatory_optional']})\n"

    response = call_openai(parameters_prompting, {"chat_history": chat_history, "question": question,
                                                          "criteria": criteria, "required_params": params_input})
    rcm = RedisCacheManager()
    rcm.connect()
    rcm.add_is_order_creation(user_id, action_id)
    return True, response