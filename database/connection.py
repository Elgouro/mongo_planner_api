from beanie import init_beanie, PydanticObjectId
from models.users import User
from models.event import Event
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, List, Any
from pydantic import BaseModel
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_NAME: str 
    debug: bool = False
    DATABASE_URL: str

    class Config:
        env_file = ".env"  # Spécifiez le nom du fichier .env

# Utilisation des paramètres
settings = Settings()
class Database:
    def __init__(self, model):
        self.model = model
    async def save(self, document) -> dict:
        await self.model.create(document)
    
    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True
    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc_id = id
        des_body = body.dict()
        des_body = {k: v for k, v in des_body.items() if v is not None}
        update_query = {"$set": {field: value for field, value in des_body.items()}}
        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc