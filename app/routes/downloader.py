from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from app.services.yt import download_and_merge_youtube_video
from app.models.schemas import DownloadRequest
import os

router = APIRouter()

@router.post('/download')
async def download_video(body: DownloadRequest):
    url = body.url.strip()
    
    if not url:
        return {'error': 'URL is required'}
    
    try:
        output_path = download_and_merge_youtube_video(url)
        filename = os.path.basename(output_path)
        # return FileResponse(output_path, media_type='video/mp4', filename=output_path.split('/')[-1])
        return {
            'message': 'Download complete',
            'filename': filename,
            'path': f'files/{filename}'
        }
    except Exception as e:
        return {'error': str(e)}