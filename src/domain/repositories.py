from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Pieza
from bson import ObjectId

class IPiezaRepository(ABC):

    @abstractmethod
    async def get_all(self) -> List[Pieza]:
        pass

    @abstractmethod
    async def get_by_id(self, pieza_id: str) -> Optional[Pieza]:
        pass

    @abstractmethod
    async def add(self, pieza: Pieza) -> Pieza:
        pass

    # Add other necessary methods like update, delete etc. if needed