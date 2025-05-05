from typing import List, Optional
from src.domain.models import Pieza
from src.domain.repositories import IPiezaRepository

class PiezaUseCases:
    def __init__(self, repository: IPiezaRepository):
        self.repository = repository

    async def get_all_piezas(self) -> List[Pieza]:
        return await self.repository.get_all()

    async def get_pieza_by_id(self, pieza_id: str) -> Optional[Pieza]:
        return await self.repository.get_by_id(pieza_id)

    async def add_pieza(self, pieza: Pieza) -> Pieza:
        # Add any business logic/validation before saving if needed
        return await self.repository.add(pieza)

    # Add other use cases corresponding to repository methods