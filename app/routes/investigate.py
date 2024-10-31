from fastapi import APIRouter, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os
import json
import instaloader
import asyncio
import logging
from app.services.instaloader_service import get_profile, download_photo
from app.services.sentiment_analysis_service import analyze_sentiment
from app.services.image_analysis_service import analyze_image_quality

# Configuración de logging para asegurar que los mensajes aparezcan en la consola
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
storage_path = "app/storage"

# Diccionario para almacenar mensajes de progreso por usuario
progress_messages = {}

@router.post("/investigate", response_class=HTMLResponse)
async def investigate_instagram(request: Request, background_tasks: BackgroundTasks, instagram_account: str = Form(...), num_photos: int = Form(20)):
    logging.debug(f"Investigación iniciada para la cuenta: {instagram_account} con {num_photos} fotos")
    await process_instagram_account(instagram_account, request, num_photos)
    
    return RedirectResponse(url=f"/results/{instagram_account}", status_code=303)

async def process_instagram_account(instagram_account: str, request: Request, num_photos: int):
    logging.debug("Iniciando análisis de cuenta Instagram")
    L = instaloader.Instaloader()
    progress_messages[instagram_account] = []

    try:
        profile = instaloader.Profile.from_username(L.context, instagram_account)
        posts = profile.get_posts()
        photos_data = []
        likes_list = []
        count = 0

        for post in posts:
            if count >= num_photos:
                break
            count += 1
            logging.debug(f"Loading picture {count}...")

            if not hasattr(post, 'mediaid') or not hasattr(post, 'url') or not hasattr(post, 'date'):
                logging.debug(f"Post {count} lacks necessary attributes.")
                continue

            unique_id = f"{instagram_account}_{post.mediaid}"
            try:
                image_path = os.path.join(storage_path, unique_id)
                L.download_pic(image_path, post.url, post.date)
                logging.debug(f"Completed picture {count}.")
            except Exception as e:
                logging.error(f"Error descargando la imagen {count}: {str(e)}")
                continue

            image_file_with_extension = f"{unique_id}.jpg"
            try:
                image_quality = analyze_image_quality(os.path.join(storage_path, image_file_with_extension))
            except Exception as e:
                image_quality = 0
                logging.error(f"Error en análisis de calidad para {count}: {str(e)}")

            description = post.caption or ""
            try:
                if description:
                    logging.debug(f"**Calling analyze_sentiment for: '{description[:50]}...'**")
                    sentiment = analyze_sentiment(description)
                    logging.debug(f"Sentiment for description '{description[:50]}...': {sentiment}")
                else:
                    sentiment = "Neutro"
                progress_messages[instagram_account].append(f"Sentimiento de la imagen {count}: {sentiment}")
            except Exception as e:
                sentiment = "Neutro"
                logging.error(f"Error en análisis de sentimiento para descripción {count}: {str(e)}")

            likes_list.append(post.likes)
            photo_info = {
                "image_url": f"/static/storage/{image_file_with_extension}",
                "likes": post.likes,
                "date": post.date.strftime("%Y-%m-%d"),
                "description": description,
                "hashtags": post.caption_hashtags,
                "quality_score": image_quality,
                "sentiment": sentiment
            }
            photos_data.append(photo_info)
            await asyncio.sleep(0.1)

        average_likes = sum(likes_list) / len(likes_list) if likes_list else 0

        for photo in photos_data:
            scoring = []
            if photo["likes"] > average_likes:
                scoring.append("good")
            else:
                scoring.append("bad")
            if photo["quality_score"] > 50:
                scoring.append("good")
            else:
                scoring.append("bad")
            if photo["sentiment"] == "POSITIVE":
                scoring.append("good")
            elif photo["sentiment"] == "NEGATIVE":
                scoring.append("bad")
            bad_count = scoring.count("bad")
            photo["global_scoring"] = "bad" if bad_count >= 2 else "good"

        json_filename = f"{instagram_account}.json"
        json_path = os.path.join(storage_path, json_filename)
        if photos_data:
            logging.debug(f"Guardando archivo JSON en: {json_path}")
            with open(json_path, "w") as f:
                json.dump(photos_data, f, indent=4)
            logging.debug(f"Archivo JSON guardado correctamente: {json_path}")
        else:
            logging.debug(f"No se han procesado fotos correctamente para {instagram_account}")

        progress_messages[instagram_account].append("Análisis completado exitosamente.")
        return RedirectResponse(url=f"/results/{instagram_account}", status_code=303)

    except Exception as e:
        logging.error(f"Error en el análisis: {str(e)}")
