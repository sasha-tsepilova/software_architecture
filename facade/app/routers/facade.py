import os
import requests
from fastapi import APIRouter
import json

router = APIRouter()
# global uuid_counter
uuid_counter = 1


@router.get('/')
def get_messages():
    logging = requests.get(os.environ['LOGGING_MICROSERVICE']).text[1:-1]
    messages = requests.get(os.environ['MESSAGE_MICROSERVICE']).text[1:-1]
    result = logging + messages
    return result

@router.post('/', status_code=201)
def post_messages(message:str):
    global uuid_counter
    response = requests.post(os.environ['LOGGING_MICROSERVICE'], json = {"uuid": uuid_counter, "message":message})
    uuid_counter += 1
    return message