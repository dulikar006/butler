from clients.openai_client import call_openai
from clients.postgres_client import PostgresClient
from database.order_manager import OrderManager
from database.redis_cache_manager import RedisCacheManager
from helpers.history_helpers import update_history
from helpers.json_helper import convert_to_json
from utilities.prompts import order_details_validation, action_fields


def extract_whatsapp_data_for_order_creation(customer_name, sms_sid, category, user_response, chat_history):
    pc = PostgresClient()
    pc.connect()
    sql = f'select distinct name, fields from public.actions where id = {int(category)}'
    result = pc.fetch_one(sql)
    params_input = ""
    order_category = result[0]
    for item in result[1]:
        params_input += f"{item['detail']} (Example: {item['example']}, {item['mandatory_optional']})\n"

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

    if (isinstance(order_details, bool) and order_details is True) or (isinstance(order_details, str) and order_details == 'True'):
        om = OrderManager()
        om.store_table_row(customer_name, str(order_creation_details), order_category)

        redis_manager = RedisCacheManager()
        redis_manager.connect()
        redis_manager.delete_order_creation(sms_sid)


        response = f'''Your order for {order_category} been created under below details sir. Enjoy your stay.
        {order_creation_details}'''

        update_history(sms_sid, user_response, response)
        return response

    update_history(sms_sid, user_response, response)
    return response

