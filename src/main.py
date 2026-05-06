from fastapi import FastAPI
from src.interface_adapters.controllers.email_controller import router as email_router

app = FastAPI()

app.include_router(email_router, prefix="/api")


@app.get("/")
async def root():
    return {"status": "ok"}
