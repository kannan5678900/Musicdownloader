import os
import requests as r
import wget
from random import randint
from pyrogram import Client, filters
from plugins.google import get_text

WALL_API = os.environ.get("WALL_API", None)

@Client.on_message(filters.command(["wall"]))
async def wall(client, message):
    msg = await message.reply("processing...")
    chat_id = message.from_user.id
    wall = get_text(message)
    if not wall:
        await msg.edit("Give me Something")
        return
    json_rep = r.get(f"https://wall.alphacoders.com/search.php?search={wall}").json()
    if not json_rep.get("success"):
        await msg.edit(f"An error occurred")
    else:
        wallpapers = json_rep.get("wallpapers")
        if not wallpapers:
            await msg.edit("No results found! Refine your search.")
            return
        index = randint(0, len(wallpapers) - 1)  # Choose random index
        wallpaper = wallpapers[index]
        wallpaper1 = wallpaper.get("url_image")
        go = wget.download(wallpaper1)
#        wallpaper = wallpaper.replace("\\", "")
        caption = f"{wall}"
        await client.send_photo(chat_id, photo=go, caption="Preview", timeout=60, quote=True)
        await client.send_document(chat_id, document=wallpaper, filename="wallpaper", caption=caption, quote=True, timeout=60)
        await msg.delete()
