import os
import yt-dlp
from pyrogram import Client, filters

from plugins.google import get_text

@Client.on_message(filters.command(["down"]))
async def down(client, message):
    msg = await message.reply("Processing...")
    query = get_text(message)
    video = {}
    try:
        with yt_dlp.YoutubeDL(video) as ydl:
            he = ydl.download(query)
        await client.send_file(he)
             
