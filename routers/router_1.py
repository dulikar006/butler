from fastapi import APIRouter, Request, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

from helpers.load_response import generate_response
from transformers.process_input_transformer import extract_whatsapp_data

# import src.auth as auth
# from src.models import Compute, Compute_all, Mode, Results

router = APIRouter(prefix="/whatsapp")


@router.post("/get_message")
async def whatsapp_reply(request: Request):
    # Get the incoming message
    form_data = await request.form()
    form_dict = dict(form_data)

    response = extract_whatsapp_data(form_dict)

    if response:
        # Create a Twilio response object
        resp = MessagingResponse()
        resp.message(response)
        # Return the TwiML response as a string
        return Response(content=str(resp), media_type="text/xml")


@router.post("/get_message_test")
def whatsapp_reply(Body: str = Form(...)):
    print('WhatsApp message hit and started')
    incoming_message = Body.lower()
    print(f'Incoming message: {incoming_message}')
    reply = generate_response(incoming_message)
    resp = MessagingResponse()
    resp.message(reply)
    return Response(content=str(resp), media_type="text/xml")

# @router.post("/compute/", response_model=Compute)
# def compute(
#     number: int,
#     mode: Mode = "SUM",
#     db: DB = Depends(get_db),
#     authorized: bool = Depends(auth.validate),
# ) -> Compute:
#     db_num = db.get_number()
#
#     if mode == "SUM":
#         result = Results(addition=(number + db_num))
#     elif mode == "SUB":
#         result = Results(subtraction=(number - db_num))
#     elif mode == "PROD":
#         result = Results(multiplication=(number * db_num))
#     elif mode == "ALL":
#         result = Results(
#             addition=(number + db_num),
#             subtraction=(number - db_num),
#             multiplication=(number * db_num),
#         )
#     else:
#         raise HTTPException(status_code=404, detail="Incorrect mode")
#
#     returns = Compute(db_number=db_num, results=result)
#     return returns
