from fastapi import APIRouter
from ..models.logging import Message

router = APIRouter()

logging_map = {}

@router.get('/')
def return_logs():
    map_values = logging_map.values()
    return (' ').join(map_values)

@router.post('/', status_code=201)
def record_log(message:Message):
    global logging_map
    print("Got a new message")
    print(f"UUID={message.uuid} with message={message.message}")
    logging_map[message.uuid] = message.message
    return message