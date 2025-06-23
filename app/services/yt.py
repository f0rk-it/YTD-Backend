import os
import uuid
import subprocess
import tempfile
from yt_dlp import YoutubeDL
from app.utils.filename import sanitize_filename

FFMPEG = 'ffmpeg'
OUTPUT_DIR = 'downloads'
os.makedirs(OUTPUT_DIR, exist_ok=True)

COOKIES_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'cookies', 'cookies.txt')
print(f"Using cookies from: {COOKIES_PATH}")

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
        'cookies': COOKIES_PATH,
        'outtmpl': video_temp,
        'quiet': True,
        'no_warnings': True,
        'http_headers' : {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
        }
    }
    
    audio_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio',
        'cookies': COOKIES_PATH,
        'outtmpl': audio_temp,
        'quiet': True,
        'no_warnings': True,
        'http_headers' : {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
        }
    }
    
    try:
        with YoutubeDL(video_opts) as ydl:
            ydl.download([url])
        
        with YoutubeDL(audio_opts) as ydl:
            ydl.download([url])
            
        merge_command = [
            FFMPEG,
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