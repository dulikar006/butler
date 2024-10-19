from logging import getLogger

from fastapi import Depends, FastAPI, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from starlette.middleware.sessions import SessionMiddleware
from starlette.templating import Jinja2Templates

import auth as auth
from routers import router_whatsapp, router_admin

from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request

logger = getLogger(__name__)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

templates = Jinja2Templates(directory="templates")

# Hardcoded credentials for simplicity
USERNAME = "admin"
PASSWORD = "password"

@app.get("/butler", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == USERNAME and password == PASSWORD:
        request.session["user"] = username
        return RedirectResponse(url="/admin", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})


# Route to display the company profile
@app.get("/", response_class=HTMLResponse)
async def get_table(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/test-auth/")
async def test(authorized: bool = Depends(auth.validate)):
    """
    Check the autentication tocken
    """
    return {"message": "Authentication success!"}


# Import all the routers that you need
app.include_router(router_whatsapp.router)
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