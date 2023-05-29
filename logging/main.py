from fastapi import FastAPI
from app.routers import logging
from app.services.logging import register_for_consul
import os
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

@app.on_event("startup")
def startup_event():
    register_for_consul(os.environ["SERVICE_NAME"])


@app.get('/')
def health_check():
    return {"status": "OK"}