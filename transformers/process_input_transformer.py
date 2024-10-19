import json

from clients.openai_client import call_openai, llm
from clients.postgres_client import PostgresClient
from clients.twillio_client import TwillioClient
from database.redis_cache_manager import RedisCacheManager
from helpers.history_helpers import get_chat_history, update_history
from helpers.json_helper import convert_to_json
from helpers.load_response import generate_response
from transformers.order_creation_transformer import extract_whatsapp_data_for_order_creation
from utilities.prompts import action_identification, action_route, parameters_prompting, reconsider_order_creation


def extract_whatsapp_data(data: dict, customer_details: dict, current_date_time: str):
    profile_name = data.get('ProfileName')
    body = data.get('Body')
    _, phone_number = data.get('From').split('+')

    # account_sid = data.get('AccountSid')
    # sms_message_sid = data.get('SmsMessageSid')
    # message_type = data.get('MessageType')
    # sms_sid = data.get('SmsSid')
    # wa_id = data.get('WaId')
    # sms_status = data.get('SmsStatus')
    # to = data.get('To')
    # num_segments = data.get('NumSegments')
    # referral_num_media = data.get('ReferralNumMedia')
    # message_sid = data.get('MessageSid')
    # from_whatsapp = data.get('From')
    # api_version = data.get('ApiVersion')
    # attachment_description = None

    if data.get('NumMedia') != '0' and data.get('MediaContentType0'):
        media_content_type = data.get('MediaContentType0')
        num_media = data.get('NumMedia')
        media_url = data.get('MediaUrl0')
        attachment_description = process_attachment_message(media_content_type, num_media, media_url, body)

    all_chat_history = get_chat_history(phone_number)# get chat history
    chat_history = add_customer_details_to_chat(all_chat_history[-5:], customer_details)

    # check if the message is part of order creation process
    redis_manager = RedisCacheManager()
    redis_manager.connect()
    category = redis_manager.is_order_creation(phone_number)

    if isinstance(category, list) and len(category) > 0:
        category = category[0]
        if category != 0 or "0" not in category:

            #get corrosponding details for category id
            pc = PostgresClient()
            pc.connect()
            sql = f'select distinct name, fields from public.actions where id = {int(category)}'
            result = pc.fetch_one(sql)
            order_category = result[0]
            order_parameters = result[1]

            # check if current question is about the booking or completely different, if different, ask still want to
            # continue with the order
            proceed_order, response = cancel_order_creation(order_category, body, chat_history)

            if proceed_order == 0 or "0" in proceed_order or body == 'Ignore': #if dont want to continue with the order
                if body == 'Ignore':
                    response = llm(f"""{response} -  convert this message to inform the customer that current ongoing order mentioned in the message been cancelled.
                                    Make sure to highlight the current ongoing message description and that it has been cancelled.
                                    Only return updated message.
                                    Do not hallucinate or add extra content or guidance.
                                     """)

                redis_manager.delete_order_creation(phone_number)
                response += "\n - Shalini, Careline Agent."
                update_history(phone_number, body, response)
                return response

            elif (proceed_order == 1 or "1" in proceed_order) and body != 'Continue': #asking if still want to continue with the order
                response = llm(f"""{response} -  convert this message to ask if want to continue with current ongoing order mentioned in the message.
                Make sure to highlight the current ongoing message description.
                Only return updated message.
                 """)
                update_history(phone_number, body, response)

                tc = TwillioClient()
                tc.connect()
                tc.send_confirmation_message(response, phone_number)
                return True

            # else go to order creation
            response = extract_whatsapp_data_for_order_creation(profile_name, phone_number,
                                                                order_category, order_parameters,
                                                                body, chat_history, customer_details)
            response += "\n - Shalini, Careline Agent."
            update_history(phone_number, body, response)
            return response

    action, criteria = identify_action(chat_history, body)

    if action == 'True':

        is_category, response = route_action(phone_number, chat_history, body, criteria)

        if is_category:  # if identified action, respond to prompt required information
            update_history(phone_number, body, response)
            if isinstance(response, dict):
                response = f"Please provide these details to proceed with the order - {str(response)}"
            response += "\n - Shalini, Careline Agent."
            return response

        response = f'''I apologize, but I’m unable to assist with your request on {criteria} at the moment. However, I’ve informed my manager, and they will be in touch with you shortly. Please feel free to let me know if there’s anything else I can assist you with in the meantime.'''
        tc = TwillioClient()
        tc.connect()
        tc.send_message(
            f"Hi Mr.Malaka, Our guest is requesting an action on {criteria}. Can you please do the needful. \n Guest Details: {customer_details} \n \n - Shalini, Careline Agent.",
            '94772608766')

    else:
        response = generate_response(body, current_date_time, chat_history=chat_history)

    update_history(phone_number, body, response)

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

    print(f'required fields - {params_input}')
    print(f'chat history - {chat_history}')

    response = call_openai(parameters_prompting, {"chat_history": chat_history, "question": question,
                                                  "criteria": criteria, "required_params": params_input})
    rcm = RedisCacheManager()
    rcm.connect()
    rcm.add_is_order_creation(user_id, action_id)
    return True, response


def cancel_order_creation(category, body, chat_history):
    json_string = call_openai(reconsider_order_creation, {"chat_history": chat_history, "category":category, "question": body})
    result_dict = convert_to_json(json_string)
    action = result_dict.get('action')
    response = result_dict.get('response')
    return action, response


def add_customer_details_to_chat(chat_hsitory, customer_details):
    formatted_chat = json.dumps(chat_hsitory, indent=4)

    return f"""customer details: {str(customer_details)}
    
    chat_history: {formatted_chat}

            """

