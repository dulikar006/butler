import atexit

from fastapi import APIRouter, Depends, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from typing import List

from database.admin_manager import AdminManager
from database.order_manager import OrderManager

router = APIRouter(prefix="/admin")

router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
# Initialize the AdminManager
admin_manager = AdminManager()
order_manager = OrderManager()

# Route to display the table
@router.get("/", response_class=HTMLResponse)
def get_table(request: Request):
    table_data = order_manager.get_table_data()  # Call the method synchronously
    return templates.TemplateResponse("index.html", {"request": request, "table_data": table_data})


# Use dependency injection for the database session
@router.get("/customers")
async def get_customers(request: Request, limit: int = 100, db: AsyncSession = Depends(admin_manager.get_db_session)):
    customers = await admin_manager.fetch_all_customers(session=db, limit=limit)
    return customers
    # return templates.TemplateResponse("index.html", {"request": request, "customers": customers})

@router.post("/add-customer")
async def create_customer(
    name: str = Form(...),
    phone_number: str = Form(...),
    room_number: int = Form(...),
    checkout_date: str = Form(...),
    db: AsyncSession = Depends(admin_manager.get_db_session)
):
    new_customer = await admin_manager.add_customer(session=db, name=name, phone_number=phone_number,
                                                    room_number=room_number, checkout_date=checkout_date)
    return RedirectResponse(url="/admin", status_code=303)

@router.post("/upload-file")
async def handle_upload_file(
    criteria: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(admin_manager.get_db_session)
):
    file_data = await admin_manager.upload_file(session=db, criteria=criteria, description=description, filename=file.filename)
    return RedirectResponse(url="/admin", status_code=303)

@router.post("/upload-brochures-file")
async def handle_upload_brochures(
    criteria: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(admin_manager.get_db_session)
):
    brochure_data = await admin_manager.upload_brochures(session=db, criteria=criteria, description=description, filename=file.filename)
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

@atexit.register
def cleanup():
    order_manager.close()