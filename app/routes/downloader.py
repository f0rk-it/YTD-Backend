from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import FileResponse
from app.services.yt import download_and_merge_youtube_video
from app.models.schemas import DownloadRequest
import os
from yt_dlp import YoutubeDL
import time

router = APIRouter()

def delete_file_later(path: str):
    time.sleep(10)
    if os.path.exists(path):
        print(f'Removing temporary file: {path}')
        os.remove(path)
        print(f'Temporary file {path} removed successfully.')

@router.post('/download')
async def download_video(body: DownloadRequest, background_tasks: BackgroundTasks):
    url = body.url.strip()
    
    if not url:
        return {'error': 'URL is required'}
    
    try:
        output_path = download_and_merge_youtube_video(url)
        filename = os.path.basename(output_path)
        print(f'Downloaded video: {filename}')
        
        # Schedule cleanup after response is sent
        background_tasks.add_task(delete_file_later, output_path)
        
        # Serve the file as a response
        return FileResponse(path=output_path, media_type='video/mp4', filename=filename, background=background_tasks)
    
    except Exception as e:
        return {'error': str(e)}
    
@router.post('/metadata')
async def get_metadata(body: DownloadRequest):
    with YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
        try:
            info = ydl.extract_info(body.url.strip(), download=False)
            print(f'Title: {info.get('title')}')
            print(f'Uploader: {info.get("uploader")}')
            print(f'Thumbnail: {info.get("thumbnail")}')
            return {
                'title': info.get('title'),
                'channel': info.get('uploader'),
                'thumbnail': info.get('thumbnail')
            }
        except Exception as e:
            return {'error': str(e)}