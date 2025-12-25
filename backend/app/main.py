from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title="q-rate API")

@app.get("/")
async def root():
    return {"message": "Welcome to q-rate API"}
