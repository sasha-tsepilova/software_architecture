from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def message():
    return "Not implemented yet"