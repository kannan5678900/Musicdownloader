import os
import requests as r
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
    json_rep = r.get(f"https://wall.alphacoders.com/api2.0/get.php?auth={WALL_API}&method=search&term={wall}").json()
    if not json_rep.get("success"):
        await msg.edit(f"An error occurred! Report this @{SUPPORT_CHAT}")
    else:
        wallpapers = json_rep.get("wallpapers")
        if not wallpapers:
            await msg.edit("No results found! Refine your search.")
            return
        index = randint(0, len(wallpapers) - 1)  # Choose random index
        wallpaper = wallpapers[index]
        wallpaper = wallpaper.get("url_image")
        wallpaper = wallpaper.replace("\\", "")
        caption = f"{wall}"
        await client.send_photo(chat_id, photo=wallpaper, caption="Preview", timeout=60, quote=True)
        await client.send_document(chat_id, document=wallpaper, filename="wallpaper", caption=caption, quote=True, timeout=60)
        await msg.delete()
