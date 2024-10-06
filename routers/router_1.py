from fastapi import APIRouter, Request, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

from helpers.load_response import generate_response
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

    customer_details = check_eligibility(form_dict.get('From'))
    if not customer_details:
        return None
    form_data["customer_details"] = customer_details

    try:
        response = extract_whatsapp_data(form_dict)
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

    form_data = {'ProfileName': 'Isuri', 'Body': incoming_message, 'AccountSid': 'test2309239802091238'}

    customer_details = check_eligibility('6582641468')
    if not customer_details:
        return None
    form_data["customer_details"] = customer_details



    response = extract_whatsapp_data(form_data)
    # response = execute_agent(data)
    if response:
        # Create a Twilio response object
        resp = MessagingResponse()
        resp.message(response)
        # Return the TwiML response as a string
        return Response(content=str(resp), media_type="text/xml")

