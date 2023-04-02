import os
from fastapi import APIRouter
from ..services.facade import get_all_messages, record_message

router = APIRouter()

@router.get('/')
def get_messages():
    return get_all_messages()

@router.post('/', status_code=201)
def post_messages(message:str):
    return record_message(message)