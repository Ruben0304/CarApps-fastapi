import uvicorn
from src.presentation.api import app

if __name__ == "__main__":
    # Asegúrate de que MongoDB esté corriendo antes de iniciar la app
    # Puedes añadir lógica aquí para verificar la conexión si es necesario
    print("Iniciando servidor FastAPI...")
    print("Accede a la documentación en http://127.0.0.1:8000/docs")
    uvicorn.run("src.presentation.api:app", host="127.0.0.1", port=8000, reload=True)