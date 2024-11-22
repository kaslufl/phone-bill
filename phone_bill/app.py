from http import HTTPStatus

from fastapi import FastAPI

from phone_bill.core.external.api import api_controller

app = FastAPI()

app.include_router(api_controller.router)


@app.get("/", status_code=HTTPStatus.OK)
def hello_world():
    return {"message": "Hello World!"}
