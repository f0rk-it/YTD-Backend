from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import downloader

app = FastAPI(title='YouTube Downloader API')

origins = [
    'http://localhost:5173',  # Frontend development server
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],  # Allow all methods
    allow_headers=['*'],  # Allow all headers
)

app.include_router(downloader.router)