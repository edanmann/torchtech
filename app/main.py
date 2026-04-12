from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.routes.games import router as games_router

app = FastAPI(title="ASCENDANCY MVP", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(games_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def home() -> FileResponse:
    return FileResponse("app/static/index.html")
