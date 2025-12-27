from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import webhook, visits
from app.worker import broker

# Lifespan context
@asynccontextmanager
async def lifespan(app: FastAPI):
    if not broker.is_worker_process:
        await broker.startup()
    yield
    if not broker.is_worker_process:
        await broker.shutdown()

app = FastAPI(title="q-rate API", lifespan=lifespan)

# CORS (Allow Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Vite default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Debug Logging Middleware
from starlette.requests import Request
from app.core.config import settings
from app.core.logging import app_logger

if settings.DEBUG:
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        app_logger.debug(f"Incoming Request: {request.method} {request.url}")
        
        # In a real "Deep Debug", we might want to log headers too
        # app_logger.debug(f"Headers: {request.headers}")
        
        response = await call_next(request)
        
        app_logger.debug(f"Response Status: {response.status_code}")
        return response



app.include_router(webhook.router, prefix="/api/v1", tags=["webhook"])
app.include_router(visits.router, prefix="/api/v1", tags=["visits"])

@app.get("/")
async def root():
    return {"message": "Welcome to q-rate API"}