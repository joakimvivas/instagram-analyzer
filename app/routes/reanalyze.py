from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
import os
import json
from app.services.instaloader_service import get_profile, download_photo
import instaloader

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
storage_path = "app/storage"

@router.post("/reanalyze")
async def reanalyze_instagram(request: Request, instagram_account: str = Form(...), num_photos: int = Form(20)):
    json_path = os.path.join(storage_path, f"{instagram_account}.json")

    # Leer el archivo JSON existente si existe
    existing_photos = []
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            existing_photos = json.load(f)

    # Obtener la fecha de la última foto guardada
    last_date = None
    if existing_photos:
        last_date = max([photo['date'] for photo in existing_photos])  # Fecha más reciente

    # Volver a realizar la investigación para obtener nuevas fotos
    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, instagram_account)

    # Obtener hasta 'num_photos' nuevas fotos
    posts = profile.get_posts()
    new_photos = []
    count = 0
    for post in posts:
        post_date = post.date.strftime("%Y-%m-%d")

        # Solo añadir fotos más recientes que la última guardada
        if last_date is None or post_date > last_date:
            unique_id = f"{instagram_account}_{post.mediaid}"
            image_path = os.path.join(storage_path, unique_id)

            # Descargar la imagen
            L.download_pic(image_path, post.url, post.date)

            # Añadir la nueva foto a la lista
            new_photos.append({
                "image_url": f"/static/storage/{unique_id}.jpg",
                "likes": post.likes,
                "date": post_date,
                "description": post.caption or "",
                "hashtags": post.caption_hashtags
            })

            count += 1
            if count >= num_photos:
                break  # Detener cuando se haya alcanzado el número seleccionado
    # Combinar las nuevas fotos con las ya existentes
    updated_photos = existing_photos + new_photos

    # Guardar las fotos actualizadas en el archivo JSON
    with open(json_path, "w") as f:
        json.dump(updated_photos, f, indent=4)

    # Redirigir a la página de resultados con las fotos actualizadas
    return templates.TemplateResponse("view_investigation.html", {
        "request": request,
        "photos": updated_photos,
        "instagram_account": instagram_account
    })