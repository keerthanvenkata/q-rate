from fastapi import FastAPI
from app.api.endpoints import webhook
from app.worker import broker

# Lifespan context is preferred over on_event in new FastAPI versions
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not broker.is_worker_process:
        await broker.startup()
    yield
    if not broker.is_worker_process:
        await broker.shutdown()

app = FastAPI(title="q-rate API", lifespan=lifespan)

app.include_router(webhook.router, prefix="/api/v1", tags=["webhook"])

@app.get("/")
async def root():
    return {"message": "Welcome to q-rate API"}
