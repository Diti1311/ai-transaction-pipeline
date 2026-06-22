from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.init_db import init_db
from app.api.jobs import router as jobs_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="AI Transaction Processing Pipeline",
    lifespan=lifespan
)

app.include_router(jobs_router)
@app.get("/")
def root():
    return {
        "message": "Backend Running"
    }