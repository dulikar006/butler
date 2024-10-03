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

reconsider_order_creation = '''
You are an expert in customer service and front desk handling in Hotel industry.
Your job is to follow below guidelines and identify the request from below chat history and question

chat history: {chat_history}

category: {category}

question: {question}


[GUIDELINES]
1. Read the chat history to get an idea on the conversation and question.
2. Focus on the question and identify if the user is continuing with the current order on given category.
3. Or Identify if user doesnt want continue with the current order.
4. Identify users intent on above mentioned points and Based on users intent return,
    - If user doesnt wants to continue with the order on given category, action - 0 , response - generate a response to ask user if want any other help.
    - If user is asking or requesting something that doesnt related to given category, action - 1 , response - generate a response to ask user if want to continue with order on current category or not.
    - If none of the above are true , action - 2, response - empty
[GUIDELINES END]

- do not invent new values or hallucinate.
- Do not return code.
- Do not return descriptions.
- Output should be a dictionary, not a dictionary list.

return output in below JSON format:
result:["action": "", "response": ""]
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

action_route = '''
You are an expert in customer service and front desk handling in Hotel industry.
Your job is to follow below guidelines and identify the request action belongs to which category from below chat history and question.

chat history: {chat_history}


question: {question}


action_criteria: {criteria}


[GUIDELINES]
1. Read the chat history to get an idea on the conversation and question.
2. Focus on the question and given criteria and identify the category or criteria of the question from below list of categories.

    {action_fields}
    
3. If the question / requested action belongs to any of the above categories return relevant action_id.
4. Do not use two or more categories.
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
result:["action_id": ""]
'''

parameters_prompting = '''
You are an expert in customer service and front desk handling in Hotel industry.
Your job is to get required details from the user.

chat history: {chat_history}

question: {question}

required parameters: {required_params}

- Make sure to only ask for mentioned details in required parameters, Don't ask for anything else.
- do not invent new values or hallucinate.
- Do not return code.
- Do not return descriptions.
- Output should be response to the customer to get required parameters


return output as a human prompting data from the customer
'''

order_details_validation = '''
You are an expert in customer service and front desk handling in Hotel industry.
Your job is to follow below guidelines and identify if this user response have all the required details for order creation on given order category.

chat_history: {chat_history}

user_response: {user_response}


order_category: {order_category}

required fields to fulfill the order: {params_input}


[GUIDELINES]
1. Read the response along with chat history and order_category.
2. Identify required fields from response and chat history.
3. Check if all the required fields been answered by the user, return order_details as True else if any required field is missing return False.
4. If user answered all the required fields, generate a dictionary of values to create the order in the system as order creation details..
5. Try your best to fit response into order, if at least most important required fields can be filled, proceed with the order.
6. If user forgot to answer most of the important required field, rewrite a response to get those fields.
[GUIDELINES END]

- do not invent new values or hallucinate.
- Do not return code.
- Do not return descriptions.
- Validate the response dictionary and fix if any errors.

return output in below JSON format:
result:["order_details": "", order_creation_details: "", response: ""]
'''


json_validation_prompt = '''You are an agent working on json validation.
input_data:
{json_data}

error message while trying to convert to dictionary: {error_message}

fix and update any errors in given dictionary value.

return output in JSON format
'''