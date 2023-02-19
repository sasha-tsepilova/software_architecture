from fastapi import FastAPI
from app.routers import logging


app = FastAPI(
    title="Software Architecture Labs",
    description="Logging microservice",
    version="1.0.0",
)


app.include_router(
    logging.router,
    tags=['logging'],
    prefix="/logging",
)


@app.get('/')
def health_check():
    return {"status": "OK"}