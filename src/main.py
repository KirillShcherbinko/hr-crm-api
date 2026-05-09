# src/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.interface_adapters.controllers.auth_controller import router as auth_router
from src.interface_adapters.controllers.users_controller import router as users_router
from src.interface_adapters.controllers.candidates_controller import router as candidates_router
from src.interface_adapters.controllers.vacancies_controller import router as vacancies_router
from src.interface_adapters.controllers.pipeline_controller import router as pipeline_router
from src.interface_adapters.controllers.emails_controller import router as emails_router
from src.interface_adapters.controllers.analytics_controller import router as analytics_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="HR CRM API",
    description="Веб-сервис для автоматизации работы HR-отделов (ATS-система)",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(
    candidates_router,
    prefix="/api/v1/candidates",
    tags=["Candidates"])
app.include_router(
    vacancies_router,
    prefix="/api/v1/vacancies",
    tags=["Vacancies"])
app.include_router(
    pipeline_router,
    prefix="/api/v1/pipeline-templates",
    tags=["Pipeline Templates"])
app.include_router(emails_router, prefix="/api/v1/emails", tags=["Emails"])
app.include_router(
    analytics_router,
    prefix="/api/v1/analytics",
    tags=["Analytics"])


# 🩺 Health Check
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "service": "hr-crm-api"}
