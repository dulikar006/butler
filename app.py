from logging import getLogger

from fastapi import Depends, FastAPI, Form
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

import auth as auth
from database.order_manager import OrderManager
from database.redis_cache_manager import RedisCacheManager
from routers import router_1, router_admin

from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request

logger = getLogger(__name__)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Route to display the table
@app.get("/", response_class=HTMLResponse)
async def get_table(request: Request):
    return
    # redis_manager = RedisCacheManager()
    # redis_manager.connect()
    # table_data = redis_manager.get_table_data()
    # return templates.TemplateResponse("index.html", {"request": request, "table_data": table_data})

# Route to add a new row
@app.post("/add", response_class=HTMLResponse)
async def add_row(name: str = Form(...), description: str = Form(...), criteria: str = Form(...)):
    om = OrderManager()
    om.store_table_row(name, description, criteria)
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete-all", response_class=HTMLResponse)
async def delete_all_rows():
    om = OrderManager()
    om.delete_all_rows()
    return RedirectResponse(url="/", status_code=303)

@app.get("/test-auth/")
async def test(authorized: bool = Depends(auth.validate)):
    """
    Check the autentication tocken
    """
    return {"message": "Authentication success!"}


# Import all the routers that you need
app.include_router(router_1.router)
app.include_router(router_admin.router)


# # Main function to execute FastAPI
# if __name__ == "__main__":
#     """
#     Run the main only for debugging purpose, as it is assigning a
#     random (free) port to run the API.
#
#     In a production set-up please run the API in its container
#     or call uvicorn directly from the CLI:
#     uvicorn src.app:app --host 0.0.0.0 --port {DESIRED PORT}
#     """
#     import uvicorn
#
#     from src.utilities import find_free_port
#
#     port = find_free_port()
#     logger.info(f"Running API on port: {port}")
#     uvicorn.run("src.app:app", host="0.0.0.0", port=port, reload=True)


#
# if __name__ == '__main__':
#     uvicorn.run('main:app', host='0.0.0.0', port=8000)