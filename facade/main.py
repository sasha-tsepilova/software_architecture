from fastapi import FastAPI
from app.routers import facade


app = FastAPI(
    title="Software Architecture Labs",
    description="Facade microservice",
    version="1.0.0",
)


app.include_router(
    facade.router,
    tags=['facade'],
    prefix="/facade",
)


@app.get('/')
def health_check():
    return {"status": "OK"}