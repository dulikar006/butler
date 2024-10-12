from fastapi import APIRouter, Request, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

from helpers.datetime_helper import get_current_time
from transformers.check_customer_status import check_eligibility
from transformers.process_input_transformer import extract_whatsapp_data

# import src.auth as auth
# from src.models import Compute, Compute_all, Mode, Results

router = APIRouter(prefix="/whatsapp")


@router.post("/get_message")
async def whatsapp_reply(request: Request):
    # Get the incoming message
    form_data = await request.form()
    form_dict = dict(form_data)

    _, phone_number = form_dict.get('From').split('+')
    customer_details = check_eligibility(phone_number)
    current_date_time = get_current_time()
    if not customer_details:
        return None

    try:
        response = extract_whatsapp_data(form_dict, customer_details, current_date_time)
    except:
        response = None

    # response = execute_agent(data)

    if response:
        # Create a Twilio response object
        resp = MessagingResponse()
        resp.message(response)
        # Return the TwiML response as a string
        return Response(content=str(resp), media_type="text/xml")

    response = f"All our agents are busy at the moments, Can you please reconnect with us in few seconds..\n - Careline Service."
    resp = MessagingResponse()
    resp.message(response)
    # Return the TwiML response as a string
    return Response(content=str(resp), media_type="text/xml")


@router.post("/get_message_test")
def whatsapp_reply(Body: str = Form(...)):
    print('WhatsApp message hit and started')
    incoming_message = Body.lower()

    form_data = {'ProfileName': 'Isuri', 'Body': incoming_message, 'AccountSid': 'test2309239802091238', 'From': '+658879926'}
    current_date_time = get_current_time()
    customer_details = check_eligibility('6588739926')
    if not customer_details:
        return None
    form_data["customer_details"] = customer_details

    response = extract_whatsapp_data(form_data, customer_details, current_date_time)
    # response = execute_agent(data)
    if response:
        # Create a Twilio response object
        resp = MessagingResponse()
        resp.message(response)
        # Return the TwiML response as a string
        return Response(content=str(resp), media_type="text/xml")

