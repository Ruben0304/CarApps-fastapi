import motor.motor_asyncio
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv() # Carga las variables de entorno desde .env

class Settings(BaseSettings):
    mongo_details: str = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")
    database_name: str = os.getenv("DATABASE_NAME", "car_parts_db")

settings = Settings()

client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_details)
database = client[settings.database_name]

pieza_collection = database.get_collection("piezas")

async def get_database():
    return database