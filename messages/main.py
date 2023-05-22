from fastapi import FastAPI
from app.routers import messages
import os
import asyncio
# from aiokafka import AIOKafkaConsumer
import app.services.messages as services

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

@app.on_event("startup")
def startup_event():
    services.consume_loop()

@app.on_event("shutdown")
def shutdown_event():
    services.stop_consumer()
