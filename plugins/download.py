import os
import yt_dlp
import ffmpeg
from pyrogram import Client, filters

from plugins.google import get_text

@Client.on_message(filters.command(["down"]))
async def down(client, message):
    msg = await message.reply("Processing...")
    query = get_text(message)
    if not query:
        await msg.edit("**എനിക്ക് എന്തെങ്കിലും താടാ**")
        return
    video = {
         "addmetadata": False,
         "key": "FFmpegMetadata",
         "prefer_ffmpeg": True,
         "geo_bypass": True,
         "nocheckcertificate": True,
         "postprocessors": [
             {
                "key": "FFmpegVideoConvertor",
                "preferredcodec": "mp4",
                "preferredquality": "720",
             },
          ],
          "outtmpl": "%(title)s.mp4",
          "quiet": True,
    }
    try:
        with yt_dlp.YoutubeDL(video) as ydl:
            he = ydl.download(query)
        await message.reply_video(video=he)
        await msg.delete()
    except Exception as e:
        await msg.edit(f'😔**Failed**\n\n__Report this Error to my [Master](https://t.me/Peterparker6)\nOr try__ : `/spotify {query}`')
        print(e)
