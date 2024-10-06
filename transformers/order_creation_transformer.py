from clients.openai_client import call_openai
from database.postgres_manager import PostgresManager
from database.redis_cache_manager import RedisCacheManager
from helpers.history_helpers import update_history
from helpers.json_helper import convert_to_json
from utilities.prompts import order_details_validation


def extract_whatsapp_data_for_order_creation(customer_name, sms_sid, order_category,
                                             order_parameters, user_response, chat_history, customer_details):
    params_input = ""

    for item in order_parameters:
        params_input += f"{item['detail']} (Example: {item['example']}, {item['mandatory_optional']})\n"

    print(f'required fields - {params_input}')
    print(f'chat history - {chat_history}')

    json_string = call_openai(order_details_validation, {"user_response": user_response,
                                                         "order_category": order_category,
                                                         "params_input": params_input,
                                                         'chat_history': chat_history[-5:]})
    result = convert_to_json(json_string)
    if isinstance(result, list):
        result = result[0]
    order_details = result.get('order_details')
    order_creation_details = result.get('order_creation_details')
    response = result.get('response')

    if (isinstance(order_details, bool) and order_details is True) or \
            (isinstance(order_details, str) and order_details == 'True'):
        om = PostgresManager()
        om.store_order_table_row(customer_name, str(order_creation_details), order_category, customer_details)

        redis_manager = RedisCacheManager()
        redis_manager.connect()
        redis_manager.delete_order_creation(sms_sid)

        response = f'''Your order for {order_category} been created under below details sir. Enjoy your stay.
        {order_creation_details}'''

        update_history(sms_sid, user_response, response)
        return response

    update_history(sms_sid, user_response, response)
    return response
