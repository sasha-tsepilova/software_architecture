from fastapi import FastAPI
from app.routers import messages


app = FastAPI(
    title="Software Architecture Labs",
    description="Messages microservice",
    version="1.0.0",
)


app.include_router(
    messages.router,
    tags=['messages'],
    prefix="/messages",
)


@app.get('/')
def health_check():
    return {"status": "OK"}