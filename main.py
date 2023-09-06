from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes.users import user_router
from routes.event import event_router
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from models.event import Event
from models.users import User
from beanie import init_beanie
from database.connection import settings

app = FastAPI()

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")


@app.get("/")
async def home():
    return f'bonjour cher Kan'


@app.on_event("startup")
async def initialize_database():
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=[Event, User]
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
