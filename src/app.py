"""
app.py
------

This file defines the entrypoint for the API. Creates the FastAPI
object and import all the endpoints defined in the diferents routers.
"""

from logging import getLogger

from fastapi import Depends, FastAPI

import auth as auth
from routers import router_1

logger = getLogger(__name__)


app = FastAPI()


@app.get("/")
async def root():
    """
    Root url of the API
    """
    return {"message": "Hello World"}


@app.get("/test-auth/")
async def test(authorized: bool = Depends(auth.validate)):
    """
    Check the autentication tocken
    """
    return {"message": "Authentication success!"}


# Import all the routers that you need
app.include_router(router_1.router)


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
#     from src.utils import find_free_port
#
#     port = find_free_port()
#     logger.info(f"Running API on port: {port}")
#     uvicorn.run("src.app:app", host="0.0.0.0", port=port, reload=True)


#
# if __name__ == '__main__':
#     uvicorn.run('main:app', host='0.0.0.0', port=8000)