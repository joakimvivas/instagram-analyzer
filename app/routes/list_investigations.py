from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
storage_path = "app/storage"

@router.get("/list-investigations")
async def list_investigations(request: Request):
    # Leer todos los archivos JSON en la carpeta storage
    investigations = [f.replace('.json', '') for f in os.listdir(storage_path) if f.endswith('.json')]
    
    return templates.TemplateResponse("list_investigations.html", {
        "request": request,
        "investigations": investigations
    })
