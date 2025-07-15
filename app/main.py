from fastapi import FastAPI
from app.routers.events import router as events_router

app = FastAPI()

app.include_router(events_router, prefix="/api/v1/events", tags=["Events"])
