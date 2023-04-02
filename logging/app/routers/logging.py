from fastapi import APIRouter
from ..models.logging import Message
from ..services.logging import return_messages, record_message

router = APIRouter()

@router.get('/')
def return_logs():
    return return_messages()

@router.post('/', status_code=201)
def record_log(message:Message):
    return record_message(message)