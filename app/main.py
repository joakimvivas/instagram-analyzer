from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.routes import investigate, reanalyze, progress, list_investigations, view_investigation

app = FastAPI()

# Configuración de las plantillas
templates = Jinja2Templates(directory="app/templates")

# Montar la carpeta de almacenamiento como estática
app.mount("/static/storage", StaticFiles(directory="app/storage"), name="storage")

# Incluir routers
app.include_router(investigate.router)
app.include_router(reanalyze.router)
app.include_router(progress.router)
app.include_router(list_investigations.router)
app.include_router(view_investigation.router)

# Devolver index.html
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
