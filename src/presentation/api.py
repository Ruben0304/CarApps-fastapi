from fastapi import FastAPI, HTTPException, Depends
from typing import List
from bson import ObjectId

from src.domain.models import Pieza
from src.application.use_cases import PiezaUseCases
from src.infrastructure.repositories import MongoPiezaRepository
from src.domain.repositories import IPiezaRepository

# Dependency Injection setup
def get_pieza_repository() -> IPiezaRepository:
    # In a real app, you might have more complex DI logic
    return MongoPiezaRepository()

def get_pieza_use_cases(repo: IPiezaRepository = Depends(get_pieza_repository)) -> PiezaUseCases:
    return PiezaUseCases(repo)

app = FastAPI(
    title="CarParts API",
    description="API para gestionar piezas de automóviles",
    version="0.1.0"
)

@app.get("/piezas", response_model=List[Pieza], tags=["Piezas"])
async def get_all_piezas(use_cases: PiezaUseCases = Depends(get_pieza_use_cases)):
    """Obtiene todas las piezas disponibles."""
    piezas = await use_cases.get_all_piezas()
    return piezas

@app.get("/piezas/{pieza_id}", response_model=Pieza, tags=["Piezas"])
async def get_pieza(pieza_id: str, use_cases: PiezaUseCases = Depends(get_pieza_use_cases)):
    """Obtiene una pieza específica por su ID de MongoDB."""
    # Validate ObjectId format before passing to use case
    if not ObjectId.is_valid(pieza_id):
        raise HTTPException(status_code=400, detail=f"'{pieza_id}' no es un ObjectId válido")

    pieza = await use_cases.get_pieza_by_id(pieza_id)
    if pieza is None:
        raise HTTPException(status_code=404, detail=f"Pieza con id {pieza_id} no encontrada")
    return pieza

@app.post("/piezas", response_model=Pieza, status_code=201, tags=["Piezas"])
async def create_pieza(pieza_data: Pieza, use_cases: PiezaUseCases = Depends(get_pieza_use_cases)):
    """Crea una nueva pieza en la base de datos."""
    # Ensure the input doesn't contain _id, let the DB generate it
    # Pydantic model should handle alias correctly, but double-check if issues arise
    # We might need to explicitly exclude '_id' or handle it in the use case/repo
    pieza_data.id = None # Ensure _id is not set before creation
    try:
        nueva_pieza = await use_cases.add_pieza(pieza_data)
        return nueva_pieza
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Log the exception e
        raise HTTPException(status_code=500, detail="Error interno al crear la pieza")

# Add other endpoints (PUT, DELETE) as needed