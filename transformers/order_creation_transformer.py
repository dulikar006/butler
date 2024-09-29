from clients.openai_client import call_openai
from database.redis_cache_manager import RedisCacheManager
from helpers.json_helper import convert_to_json
from utilities.prompts import order_details_validation, action_fields


def extract_whatsapp_data_for_order_creation(customer_name, sms_sid, category, user_response, chat_history):
    orders = {
    1: "Restaurant/Food Orders",
    2: "Shuttle/Transport Orders",
    3: "Housekeeping Orders",
    4: "Laundry Service",
    5: "Spa/Gym Booking",
    6: "Wake-Up Calls",
    7: "Event/Activity Bookings"
    }

    order_category = orders.get(int(category))

    json_string = call_openai(order_details_validation, {"user_response": user_response, "order_category": order_category,
                                                          "action_fields": action_fields, 'chat_history': chat_history})
    result_dict = convert_to_json(json_string)
    result = result_dict.get('result')
    if isinstance(result, list):
        result = result[0]
    order_details = result.get('order_details')
    order_creation_details = result.get('order_creation_details')
    response = result.get('response')

    if (isinstance(order_details, bool) and order_details is True) or (isinstance(order_details, str) and order_details == 'True'):

        redis_manager = RedisCacheManager()
        redis_manager.connect()
        redis_manager.delete_order_creation(sms_sid)

        redis_manager.store_table_row(customer_name, str(order_creation_details), order_category)

        response = f'''Your order for {order_category} been created under below details sir. Enjoy your stay.
        {order_creation_details}'''
        return response

    return response

