from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.domain.models import Pieza
from src.domain.repositories import IPiezaRepository
from .database import pieza_collection # Import the collection instance

class MongoPiezaRepository(IPiezaRepository):
    def __init__(self, collection: AsyncIOMotorCollection = pieza_collection):
        self.collection = collection

    async def get_all(self) -> List[Pieza]:
        piezas_cursor = self.collection.find()
        piezas_list = await piezas_cursor.to_list(length=None) # Get all documents
        # Convert MongoDB docs to Pieza models, handling potential None values
        return [Pieza(**pieza) for pieza in piezas_list if pieza is not None]

    async def get_by_id(self, pieza_id: str) -> Optional[Pieza]:
        if not ObjectId.is_valid(pieza_id):
            # Or raise a specific exception, e.g., InvalidIdError
            return None
        pieza_doc = await self.collection.find_one({"_id": ObjectId(pieza_id)})
        if pieza_doc:
            return Pieza(**pieza_doc)
        return None

    async def add(self, pieza: Pieza) -> Pieza:
        # Ensure we don't send the '_id' field if it's None (let MongoDB generate it)
        # Use exclude_unset=True or manually create the dict
        pieza_dict = pieza.model_dump(by_alias=True, exclude_none=True)
        if "_id" in pieza_dict and pieza_dict["_id"] is None:
            del pieza_dict["_id"] # Remove None _id before insertion

        # Ensure 'id' (aliased to id_pieza) is present
        if 'id' not in pieza_dict:
             raise ValueError("Missing required field 'id' (id_pieza)")

        result = await self.collection.insert_one(pieza_dict)
        # Fetch the newly created document to include the generated _id
        new_pieza_doc = await self.collection.find_one({"_id": result.inserted_id})
        if new_pieza_doc:
            return Pieza(**new_pieza_doc)
        # This case should ideally not happen if insertion was successful
        # Consider raising an error or logging if new_pieza_doc is None
        raise Exception("Failed to retrieve the newly added pieza")

    # Implement other methods like update, delete as needed