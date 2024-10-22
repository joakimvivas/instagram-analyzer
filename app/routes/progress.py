from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
import asyncio

router = APIRouter()

# Diccionario global para almacenar mensajes de progreso
progress_messages = {}

@router.get("/progress/{instagram_account}")
async def get_progress(instagram_account: str):
    async def event_generator():
        while True:
            if instagram_account in progress_messages:
                messages = progress_messages[instagram_account]
                for message in messages:
                    yield {"data": message}
                del progress_messages[instagram_account]
            await asyncio.sleep(1)

    return EventSourceResponse(event_generator())
