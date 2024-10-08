import atexit
import json

from fastapi import APIRouter, Depends, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from typing import List, Optional

from clients.twillio_client import TwillioClient
from database.admin_manager import AdminManager
from database.mongo_db_manager import upload_file, upload_information
from database.postgres_manager import PostgresManager

router = APIRouter(prefix="/admin")

router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
# Initialize the AdminManager
admin_manager = AdminManager()
order_manager = PostgresManager()


# Route to display the table
@router.get("/", response_class=HTMLResponse)
async def get_table(request: Request, limit: int = 100, db: AsyncSession = Depends(admin_manager.get_db_session)):
    user = request.session.get("user")
    if not user:
        return templates.TemplateResponse("login.html", {"request": request})

    table_data = order_manager.get_order_table_data()
    customers = await admin_manager.fetch_all_customers(session=db, limit=limit)
    functions = await admin_manager.fetch_distinct_functions_and_names(session=db, limit=limit)

    for row in table_data:
        if isinstance(row['customer_details'], str):
            row['customer_details'] = json.loads(row['customer_details'])

    return templates.TemplateResponse("admin.html", {
        "request": request,
        "table_data": table_data,
        "customers": customers,
        "functions": functions
    })


@router.get("/test", response_class=HTMLResponse)
async def get_table(request: Request, limit: int = 100, db: AsyncSession = Depends(admin_manager.get_db_session)):
    table_data = order_manager.get_order_table_data()
    customers = await admin_manager.fetch_all_customers(session=db, limit=limit)
    functions = await admin_manager.fetch_distinct_functions_and_names(session=db, limit=limit)

    for row in table_data:
        if isinstance(row['customer_details'], str):
            row['customer_details'] = json.loads(row['customer_details'])

    return templates.TemplateResponse("admin.html", {
        "request": request,
        "table_data": table_data,
        "customers": customers,
        "functions": functions
    })


# Use dependency injection for the database session
@router.get("/customers")
async def get_customers(request: Request, limit: int = 100, db: AsyncSession = Depends(admin_manager.get_db_session)):
    customers = await admin_manager.fetch_all_customers(session=db, limit=limit)
    return customers
    # return templates.TemplateResponse("admin.html", {"request": request, "customers": customers})


@router.post("/add-customer")
async def create_customer(
        name: str = Form(...),
        phone_number: str = Form(...),
        room_number: int = Form(...),

        # gender: str = Form(...),
        # age: str = Form(...),
        # family_members: str = Form(...),
        add_details: str = Form(...),

        checkout_date: str = Form(...),
        db: AsyncSession = Depends(admin_manager.get_db_session)
):
    new_customer = await admin_manager.add_customer(session=db, name=name, phone_number=phone_number,
                                                    room_number=room_number, checkout_date=checkout_date,
                                                    # gender=gender, age=age, family_members=family_members,
                                                    add_details=add_details
                                                    )

    tc = TwillioClient()
    tc.connect()
    # tc.send_message(
    #     f"Hi Mr.{name}, A warm welcome to Avani Kalutara Resort and Spa! We're delighted to have you with us. If there’s anything we can do to make your stay more comfortable or special, please don't hesitate to let us know. We’re here for you at every moment. ? \n - Shalini, Careline Agent.",
    #     phone_number)
    tc.send_template_message(name, "Avani Kalutara Resort and Spa", " Shalini, Careline Agent", phone_number)

    return RedirectResponse(url="/admin", status_code=303)


@router.post("/upload-file")
async def handle_upload_file(
        criteria: str = Form(...),
        description: str = Form(...),
        information: Optional[str] = Form(None),
        file: UploadFile = File(...),
        db: AsyncSession = Depends(admin_manager.get_db_session)
):
    file_data = await admin_manager.upload_file(session=db, criteria=criteria, description=description,
                                                information=information, filename=file.filename)

    if file:
        file_content = await file.read()
        upload_file(file.filename, file_content)
    if information:
        upload_information(information)

    return RedirectResponse(url="/admin", status_code=303)


@router.post("/upload-brochures-file")
async def handle_upload_brochures(
        criteria: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...),
        db: AsyncSession = Depends(admin_manager.get_db_session)
):
    brochure_data = await admin_manager.upload_brochures(session=db, criteria=criteria, description=description,
                                                         filename=file.filename)
    return RedirectResponse(url="/admin", status_code=303)


@router.post("/add-action")
async def add_action(
        f_name: str = Form(...),
        a_name: str = Form(...),
        a_description: str = Form(...),
        required_details: List[str] = Form(...),
        example_values: List[str] = Form(...),
        mandatory_optional: List[str] = Form(...),
        db: AsyncSession = Depends(admin_manager.get_db_session)
):
    action_data = await admin_manager.add_action(
        session=db,
        function=f_name,
        name=a_name,
        description=a_description,
        fields={
            "details": required_details,
            "examples": example_values,
            "mandatory_optional": mandatory_optional
        }
    )
    return RedirectResponse(url="/admin", status_code=303)

@router.post("/push-notifications")
async def push_notifications(
        p_number: str = Form(...),
        n_message: str = Form(...),
        s_ref: str = Form(...),
):

    message = n_message + ' \n  ' + s_ref
    tc = TwillioClient()
    tc.connect()
    tc.send_message(message, p_number)

    return RedirectResponse(url="/admin", status_code=303)


@atexit.register
def cleanup():
    order_manager.close()
