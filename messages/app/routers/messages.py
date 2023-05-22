from fastapi import APIRouter
from ..services.messages import get_logs

router = APIRouter()

@router.get('/')
async def message():
    return await get_logs()