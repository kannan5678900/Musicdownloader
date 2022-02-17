from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait, MessageNotModified
import requests
import wget
import asyncio
import io
import os
import time
import math
import shlex
import sys
import urllib

from plugins.google import get_text

def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"

async def progress(current, total, message, start, type_of_ps, file_name=None):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join(["🔴" for i in range(math.floor(percentage / 10))]),
            "".join(["🔘" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            try:
                await message.edit(
                    "{}\n**File Name:** `{}`\n{}".format(type_of_ps, file_name, tmp)
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass
        else:
            try:
                await message.edit("{}\n{}".format(type_of_ps, tmp))
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass

@Client.on_message(filters.command(["deezer", "dsong"]))
async def deezer(client, message: Message):
    pablo = await client.send_message(message.chat.id, "Searching the song")
    sgname = get_text(message)
    if not sgname:
        await pablo.edit("Invalid Command Syntax, Please Check Help Menu To Know More!")
        return
    link = f"https://api.deezer.com/search?q={sgname}&limit=1"
    dato = requests.get(url=link).json()
    match = dato.get("data")
    urlhp = match[0]
    urlp = urlhp.get("link")
    thums = urlhp["album"]["cover_big"]
    thum_f = wget.download(thums)
    polu = urlhp.get("artist")
    replo = urlp[29:]
    urlp = f"https://starkapi.herokuapp.com/deezer/{replo}"
    datto = requests.get(url=urlp, allow_redirects=False).json()
    mus = datto.get("url")
    sname = f"{urlhp.get('title')}.mp3"
    doc = requests.get(mus)
    await client.send_chat_action(message.chat.id, "upload_audio")
    await pablo.edit("`Downloading Song From Deezer!`")
    with open(sname, "wb") as f:
        f.write(doc.content)
    c_time = time.time()
    await pablo.edit(f"`Downloaded {sname}! Now Uploading Song...`")
    await client.send_audio(
        message.chat.id,
        audio=open(sname, "rb"),
        duration=int(urlhp.get("duration")),
        title=str(urlhp.get("title")),
        performer=str(polu.get("name")),
        thumb=thum_f,
        progress=progress,
        progress_args=(pablo, c_time, f"`Uploading {sname} Song From Deezer!`", sname),
    )
    await client.send_chat_action(message.chat.id, "cancel")
    await pablo.delete()

@Client.on_message(filters.command(["saavn"]))
async def saavn(client, message):
    msg = await message.reply_text("Downloading...")
    chat_id = message.chat.id
    query = get_text(message)
    user_id = message.from_user.id
    print(f"saavn:{query}.UserId: {user_id}")
    if not query:
        await msg.edit("**Invalid Syntax\nTry :** `/saavn Verithanam`")
        return
    if 'https://www.jiosaavn.com/song' in query:
        await msg.edit("Currently link not Support!! 😔")
        return
    link = f"https://api.deezer.com/search?q={query}&limit=1"
    dato = requests.get(url=link).json()
    match = dato.get("data")
    urlhp = match[0]
    urlp = urlhp.get("link")
    thums = urlhp["album"]["cover_big"]
    thumb = wget.download(thums)
    # await message.reply_photo(photo=thumb)
    search = f"http://starkmusic.herokuapp.com/result/?query={query}"
    saavn = requests.get(url=search, allow_redirects=False).json()
    try:
        await msg.edit(f"**Uploading Your Song...**[💥](https://telegra.ph/file/a0cfbfb334914009252b8.png)")
        for me in saavn:
            album = me['album']
            song = me['song']
            permurl = me['perma_url']
            singer = me['singers']
            dur = me['duration']
            langs = me['language']
            hidden_url = me['media_url']
            year = me['year']
            DIRCOVER = "songpicts//" + song + ".png"
#            file1 = open(DIRCOVER, "wb")
#            file1.write(thums.content)
#            file1.close()
            file = wget.download(hidden_url)
            ffile = file.replace(f"{file}", f"{song}.mp3")
            os.rename(file, ffile)
#            file1 = open(ffile, "wb")
#            file1.write(thums.content)
#            file1.close()
          
            iron_man = f"**Title** : __{song}__\n**Album** : __{album}__\n**Artist** : __{singer}__\n**Duration** : `{dur}`\n**Language** : `{langs}`\n**Released on** : `{year}`"
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton('🎧 Listen', url=f'{me["perma_url"]}')]])
            
            await client.send_chat_action(chat_id, "upload_audio")
            await message.reply_audio(audio=open(ffile, "rb"), title=song, performer=str(singer), caption=iron_man, reply_markup=buttons, quote=True)
            await msg.delete()
    except Exception as e:
        await msg.edit("⚠️ **Something went wrong.please try again**")    
        print(e)
