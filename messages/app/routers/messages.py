from fastapi import APIRouter
from ..services.messages import get_message

router = APIRouter()

@router.get('/')
def message():
    return get_message()