import os
import uuid
import subprocess
import tempfile
from yt_dlp import YoutubeDL
from app.utils.filename import sanitize_filename

FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
OUTPUT_DIR = 'downloads'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_and_merge_youtube_video(url: str) -> str:
    # Extract video info
    info_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
    }
    with YoutubeDL(info_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = sanitize_filename(info.get('title', 'video'))
        channel = sanitize_filename(info.get('uploader', 'channel'))
        filename = f"[{channel}] {title}.mp4"
    
    video_temp = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}_video.mp4")
    audio_temp = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}_audio.m4a")
    final_path = os.path.join(OUTPUT_DIR, filename)
    
    video_opts = {
        'format': 'bestvideo[height=1440][ext=mp4]/bestvideo[height<=1080][ext=mp4]',
        'outtmpl': video_temp,
        'quiet': True,
        'no_warnings': True,
    }
    
    audio_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio',
        'outtmpl': audio_temp,
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with YoutubeDL(video_opts) as ydl:
            ydl.download([url])
        
        with YoutubeDL(audio_opts) as ydl:
            ydl.download([url])
            
        merge_command = [
            FFMPEG_PATH,
            '-y',
            '-i', video_temp,
            '-i', audio_temp,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-strict', 'experimental',
            final_path
        ]
        subprocess.run(merge_command, check=True)
        return final_path
    
    finally:
        for f in (video_temp, audio_temp):
            if os.path.exists(f):
                os.remove(f)