from typing import List

from fastapi import APIRouter, Form, Depends, HTTPException
from twilio.twiml.messaging_response import MessagingResponse

from helpers.load_response import generate_response

# import src.auth as auth
# from src.models import Compute, Compute_all, Mode, Results

router = APIRouter(prefix="/Whatsapp")


@router.post("/get_response")  # ,response_class=PlainTextResponse
async def whatsapp_reply(Body: str = Form(...)):
    # Get the incoming message (no need to access `request.values` as in Flask)
    incoming_message = Body.lower()

    # Generate a response using the external function
    reply = generate_response(incoming_message)
    print(type(reply))

    # Create a Twilio response object
    resp = MessagingResponse()
    resp.message(reply)

    # Return the TwiML response as a string
    return str(resp)

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


