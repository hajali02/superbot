import yt_dlp
import os
from telegram import Update
from telegram.ext import ContextTypes

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    try:
        ydl_opts = {
            "format": "mp4",
            "outtmpl": "downloaded_video.%(ext)s",
            "noplaylist": True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        video_path = "downloaded_video.mp4"
        await update.message.reply_video(video=open(video_path, "rb"))
        os.remove(video_path)
    except Exception as e:
        await update.message.reply_text(f"خطا در دانلود ویدیو: {e}")
