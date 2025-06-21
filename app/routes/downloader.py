from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from app.services.yt import download_and_merge_youtube_video
from app.models.schemas import DownloadRequest
import os
from yt_dlp import YoutubeDL

router = APIRouter()

@router.post('/download')
async def download_video(body: DownloadRequest):
    url = body.url.strip()
    
    if not url:
        return {'error': 'URL is required'}
    
    try:
        output_path = download_and_merge_youtube_video(url)
        filename = os.path.basename(output_path)
        print(f'Downloaded video: {filename}')
        return FileResponse(path=output_path, media_type='video/mp4', filename=filename)
        # return {
        #     'message': 'Download complete',
        #     'filename': filename,
        #     'path': f'files/{filename}'
        # }
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