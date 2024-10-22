from fastapi import APIRouter, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse  # Asegúrate de que RedirectResponse esté importado
from fastapi.templating import Jinja2Templates
import os
import json
import instaloader
import asyncio
from app.services.instaloader_service import get_profile, download_photo
from app.services.sentiment_analysis_service import analyze_sentiment
from app.services.image_analysis_service import analyze_image_quality

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
storage_path = "app/storage"

# Diccionario para almacenar mensajes de progreso por usuario
progress_messages = {}

@router.post("/investigate", response_class=HTMLResponse)
async def investigate_instagram(request: Request, background_tasks: BackgroundTasks, instagram_account: str = Form(...), num_photos: int = Form(20)):
    # Iniciar el análisis en segundo plano o en tiempo real
    await process_instagram_account(instagram_account, request, num_photos)  # Si quieres ejecutarlo en tiempo real
    
    # Si prefieres en segundo plano:
    # background_tasks.add_task(process_instagram_account, instagram_account, request, num_photos)
    
    # Redirigir directamente a la página de resultados después del análisis
    return RedirectResponse(url=f"/results/{instagram_account}", status_code=303)

async def process_instagram_account(instagram_account: str, request: Request, num_photos: int):
    # Inicializar instaloader
    L = instaloader.Instaloader()

    progress_messages[instagram_account] = []

    try:
        profile = instaloader.Profile.from_username(L.context, instagram_account)

        # Comprobar si tiene al menos las fotos solicitadas
        posts = profile.get_posts()
        photos_data = []
        likes_list = []
        count = 0

        # Procesar el número de fotos seleccionado
        for post in posts:
            if count >= num_photos:
                break

            count += 1
            progress_messages[instagram_account].append(f"Loading picture {count}...")

            # Verificar si 'post' tiene los atributos necesarios
            if not hasattr(post, 'mediaid') or not hasattr(post, 'url') or not hasattr(post, 'date'):
                progress_messages[instagram_account].append(f"Error: El post {count} no tiene los atributos necesarios.")
                continue  # Saltar al siguiente post si faltan atributos

            # Generar un identificador único para la imagen
            unique_id = f"{instagram_account}_{post.mediaid}"

            try:
                # Descargar la imagen sin añadir manualmente la extensión .jpg
                image_path = os.path.join(storage_path, unique_id)
                L.download_pic(image_path, post.url, post.date)
                progress_messages[instagram_account].append(f"Completed picture {count}.")
            except Exception as e:
                progress_messages[instagram_account].append(f"Error descargando la imagen {count}: {str(e)}")
                print(f"Error descargando la imagen {count}: {str(e)}")
                continue  # Saltar al siguiente post si falla la descarga

            # Obtener la ruta correcta de la imagen descargada
            image_file_with_extension = f"{unique_id}.jpg"

            # Analizar la calidad de la imagen
            try:
                image_quality = analyze_image_quality(os.path.join(storage_path, image_file_with_extension))
            except Exception as e:
                image_quality = 0  # Poner un valor por defecto si falla el análisis
                progress_messages[instagram_account].append(f"Error en análisis de calidad para {count}: {str(e)}")

            # Analizar el sentimiento de la descripción (si existe)
            description = post.caption or ""
            try:
                if description:
                    sentiment = analyze_sentiment(description)[0]['label']  # Obtener el sentimiento
                else:
                    sentiment = "Neutro"  # Si no hay descripción, considerarlo neutro
            except Exception as e:
                sentiment = "Neutro"  # Si falla el análisis, se considera neutro
                progress_messages[instagram_account].append(f"Error en análisis de sentimiento para {count}: {str(e)}")

            # Agregar los likes al listado para calcular el average posteriormente
            likes_list.append(post.likes)

            # Agregar la información de la foto al listado con la calidad de imagen y el sentimiento
            photo_info = {
                "image_url": f"/static/storage/{image_file_with_extension}",
                "likes": post.likes,
                "date": post.date.strftime("%Y-%m-%d"),
                "description": description,
                "hashtags": post.caption_hashtags,
                "quality_score": image_quality,
                "sentiment": sentiment  # Añadir el análisis de sentimiento
            }

            photos_data.append(photo_info)
            await asyncio.sleep(0.1)  # Simular tiempo de procesamiento

        # Calcular el promedio de likes
        average_likes = sum(likes_list) / len(likes_list) if likes_list else 0

        # Aplicar las reglas para calcular el "global scoring" en cada foto
        for photo in photos_data:
            scoring = []

            # Regla 1: Likes por encima del average
            if photo["likes"] > average_likes:
                scoring.append("good")
            else:
                scoring.append("bad")

            # Regla 2: Calidad de Imagen
            if photo["quality_score"] > 50:
                scoring.append("good")
            else:
                scoring.append("bad")

            # Regla 3: Sentimiento de la Descripción
            if photo["sentiment"] == "POSITIVE":
                scoring.append("good")
            elif photo["sentiment"] == "NEGATIVE":
                scoring.append("bad")
            # Descartamos "Neutro" (no añadimos nada)

            # Contar cuántas reglas resultaron en "bad"
            bad_count = scoring.count("bad")

            # Nueva regla: si dos o más reglas son "bad", el global_scoring será "bad"
            if bad_count >= 2:
                photo["global_scoring"] = "bad"
            else:
                photo["global_scoring"] = "good"

        # Guardar en un archivo JSON
        json_filename = f"{instagram_account}.json"
        json_path = os.path.join(storage_path, json_filename)

        # Guardar el JSON solo si se han descargado fotos correctamente
        if photos_data:
            print(f"Guardando archivo JSON en: {json_path}")
            with open(json_path, "w") as f:
                json.dump(photos_data, f, indent=4)
            print(f"Archivo JSON guardado correctamente: {json_path}")
        else:
            print(f"No se han procesado fotos correctamente para {instagram_account}")

        progress_messages[instagram_account].append("Análisis completado exitosamente.")

        # Redirigir a la página de resultados
        return RedirectResponse(url=f"/results/{instagram_account}", status_code=303)

    except Exception as e:
        progress_messages[instagram_account].append(f"Error: {str(e)}")
        print(f"Error en el análisis: {str(e)}")
