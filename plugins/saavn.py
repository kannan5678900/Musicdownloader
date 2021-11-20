from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import urllib
import wget
import os

from plugins.google import get_text

def progress(current, total):
    print(f"{current * 100 / total:.1f}%")

@Client.on_message(filters.command("saavn"))
async def saavn(client, message):
    msg = await message.reply_text("`Downloading...`")
    chat_id = message.chat.id
    query = get_text(message)
    if not query:
        await msg.edit("**Invalid Syntax\nTry :** `/saavn Verithanam`")
        return
    search = f"http://starkmusic.herokuapp.com/result/?query={query}"
    saavn = requests.get(url=search).json()
    for me in saavn:
        album = me['album']
        song = me['song']
        permurl = me['perma_url']
        singer = me['singers']
        dur = me['duration']
        langs = me['language']
        hidden_url = me['media_url']
        year = me['year']
        file = wget.download(hidden_url)
        ffile = file.replace(f"{file}", f"{song}.mp3")
        iron_man = f"⚡ **Title** : __{song}__\n💫 **Album** : __{album}__\n🗣️ **Artist** : __{singer}__\n⏳ **Duration** : `{dur}`\n📋 **Language** : `{langs}`\n🔮 **Released on** : `{year}`"
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton('💥 Listen', url=f'{me["perma_url"]}')]])
        os.rename(file, ffile)
        await client.send_chat_action(chat_id, "upload_audio")
        await message.reply_audio(audio=ffile, title=song, performer=singer, caption=iron_man, reply_markup=buttons)
        await msg.delete()
        print(query)
