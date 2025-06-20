from fastapi import FastAPI
from app.routes import downloader

app = FastAPI(title='YouTube Downloader API')

app.include_router(downloader.router)