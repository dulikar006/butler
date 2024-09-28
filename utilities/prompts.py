action_identification = '''
You are an expert in customer service and front desk handling in Hotel industry.
Your job is to follow below guidelines and identify the request from below chat history and question

chat history: {chat_history}


question: {question}


[GUIDELINES]
1. Read the chat history to get an idea on the conversation and question.
2. Focus on the question and identify the category or criteria of the question.
3. Identify if this question is general inquery or action execution request.
4. If it's an action request return action as True, Else return action as False.
[GUIDELINES END]

- do not invent new values or hallucinate.
- Do not return code.
- Do not return descriptions.
- Output should be a dictionary, not a dictionary list.

return output in below JSON format:
result:["criteria": "", "action": "True or False"]
'''

action_fields = '''
Restaurant/Food Orders:
Meal type: Room Food Delivery
Menu selection: Required Menu Item Name 
Special dietary preferences: Vegan, Vegetarian, Gluten-free, etc.
Delivery time: Immediate or scheduled for later
Room number: To ensure the order is delivered to the correct room
Payment method: Room charge or pay via card/cash on delivery


Shuttle/Transport Orders:
Pickup time: When the shuttle should arrive
Pickup location: Whether it's the hotel or a nearby attraction
Drop-off location: Where the guest needs to go
Number of passengers: To ensure enough seats are available
Special requests: Baby seats, luggage assistance, etc.


Housekeeping Orders:
Service type: Full room cleaning, Towel replacement, Washroom cleaning, Bed linen change
Preferred time: Immediate or at a scheduled time
Additional requests: Extra toiletries, water bottles, etc.
Urgency level: Immediate or routine


Laundry Service:
Type of items: Clothes, bed linen, towels, etc.
Service required: Washing, ironing, dry cleaning
Pickup and delivery times: Schedule for collection and return
Special instructions: Delicate fabrics, etc.


Spa/Gym Booking:
Service type: Massage, facial, personal training session
Preferred time and date: Appointment scheduling
Special preferences: Gender preference for therapist, etc.


Wake-Up Calls:
Wake-up time: Exact time or range
Additional requests: Coffee delivery, breakfast setup


Event/Activity Bookings:
Event type: Yoga session, local tours, in-house events
Time and date: Schedule for participation
Special requests: Group bookings, special assistance
'''

action_route = '''
You are an expert in customer service and front desk handling in Hotel industry.
Your job is to follow below guidelines and identify the request action belongs to which category from below chat history and question.

chat history: {chat_history}


question: {question}


action_criteria: {criteria}


[GUIDELINES]
1. Read the chat history to get an idea on the conversation and question.
2. Focus on the question and given criteria and identify the category or criteria of the question from below list of categories.
   - Restaurant/Food Orders - 1
   - Shuttle/Transport Orders - 2
   - Housekeeping Orders -3
   - Laundry Service - 4
   - Spa/Gym Booking - 5
   - Wake-Up Calls - 6
   - Event/Activity Bookings - 7
3. If the question / requested action belongs to any of the above categories return the corresponding number of most suited category.
4. Only return most suited category's number, do not return two or more numbers.
5. If the question/action doesnt fit into any of the above mentioned categories, return 0.
[GUIDELINES END]

- do not invent new values or hallucinate.
- Do not return code.
- Do not return descriptions.
- Output should be a dictionary, not a dictionary list.
- Do not try to overfit into the category , if it doesnt fit into any categories, return 0.

return output in below JSON format:
result:["category": ""]
'''


action_route_consolidated = '''
You are an expert in customer service and front desk handling in Hotel industry.
Your job is to follow below guidelines and identify the request action belongs to which category from below chat history and question.

chat history: {chat_history}


question: {question}


action_criteria: {criteria}

required fields to fullfill the order: {action_fields}


[GUIDELINES]
1. Read the chat history to get an idea on the conversation and question.
2. Focus on the question and given criteria and identify the category or criteria of the question from below list of categories.
     - Restaurant/Food Orders - 1
   - Shuttle/Transport Orders - 2
   - Housekeeping Orders -3
   - Laundry Service - 4
   - Spa/Gym Booking - 5
   - Wake-Up Calls - 6
   - Event/Activity Bookings - 7
3. If the question / requested action belongs to any of the above categories return a response to prompt required values to place the order.
4. Only use most suited category for the response to prompt required fields, do not use two or more categories.
5. Only return most suited category's number, do not return two or more numbers.
6. If the question/action doesnt fit into any of the above mentioned categories, return 0.
[GUIDELINES END]

- do not invent new values or hallucinate.
- Do not return code.
- Do not return descriptions.
- Output should be a dictionary, not a dictionary list.
- Do not try to overfit into the category , if it doesnt fit into any categories, return 0.
- return integer for category value.

return output in below JSON format:
result:["category": "", response: ""]
'''


order_details_validation = '''
You are an expert in customer service and front desk handling in Hotel industry.
Your job is to follow below guidelines and identify if this user response have all the required details for order creation on given order category.


user_response: {user_response}


order_category: {order_category}

required fields to fullfill the order: {action_fields}


[GUIDELINES]
1. Read the response and order_category.
2. Identify required fields for given order category.
3. Check if all the required fields been answered by the user, return order_details as True else if any required field is missing return False.
4. If user answered all the required fields, generate a dictionary of values to create the order in the system as order creation details..
5. Try your best to fit response into order, if at least most important required fields can be filled, proceed with the order.
6. If user forgot to answer most of the important required field, rewrite a response to get those fields.
[GUIDELINES END]

- do not invent new values or hallucinate.
- Do not return code.
- Do not return descriptions.

return output in below JSON format:
result:["order_details": "", order_creation_details: "", response: ""]
'''


json_validation_prompt = '''You are an agent working on json validation.
input_data:
{json_data}

fix and update any errors in given dictionary value.

return output in JSON format
'''