from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os
import json

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
storage_path = "app/storage"

@router.get("/results/{username}")
async def view_investigation(request: Request, username: str):
    # Leer el archivo JSON de la investigación correspondiente
    json_path = os.path.join(storage_path, f"{username}.json")
    if not os.path.exists(json_path):
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"No se encontraron datos para el usuario {username}."
        })

    # Leer los datos del archivo JSON
    with open(json_path, "r") as f:
        photos_data = json.load(f)

    # Calcular el promedio de likes
    likes_list = [photo['likes'] for photo in photos_data]
    average_likes = sum(likes_list) / len(likes_list) if likes_list else 0

    # Pasar los datos al template de investigación
    return templates.TemplateResponse("view_investigation.html", {
        "request": request,
        "photos": photos_data,
        "average_likes": average_likes,
        "instagram_account": username
    })
