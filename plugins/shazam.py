from pyrogram import Client, filters, types
import os
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from shazamio import Shazam, exceptions, FactoryArtist, FactoryTrack

from bot import bot

shazam = Shazam()

async def edit_or_reply(message, text, parse_mode="md"):
    if message.from_user.id:
        if message.reply_to_message:
            kk = message.reply_to_message.message_id
            return await message.reply_text(
                text, reply_to_message_id=kk, parse_mode=parse_mode
            )
        return await message.reply_text(text, parse_mode=parse_mode)
    return await message.edit(text, parse_mode=parse_mode)

def getfileid(msg: Message):
    if msg.media:
        for message_type in (
            "video",
            "audio",
            "voice",
        ):
            obj = getattr(msg, message_type)
            if obj:
                setattr(obj, "message_type", message_type)
                return obj

async def recognize(self):
    return await shazam.recognize_song(path)

async def related(self, track_id):
    try:
        return (await shazam.related_tracks(track_id=track_id, limit=50, start_from=2))['tracks']
    except exceptions.FailedDecodeJson:
        return None
    
async def get_artist(self, query: str):
    artists = await shazam.search_artist(query=query, limit=50)
    hits = []
    try:
        for artist in artists['artists']['hits']:
            hits.append(FactoryArtist(artist).serializer())
        return hits
    except KeyError:
        return None

async def get_artist_tracks(self, artist_id: int):
        tracks = []
        tem = (await shazam.artist_top_tracks(artist_id=artist_id, limit=50))['tracks']
        try:
            for track in tem:
                tracks.append(FactoryTrack(data=track).serializer())
            return tracks
        except KeyError:
            return None
        
@Client.on_message(filters.command("shazam"))
async def voice_handler(client, message):
    msg = await message.reply("`Processing.. please wait for some Seconds...`")
    hello = message.reply_to_message
    if not hello:
        await msg.edit("**Please reply to Supported Media.** 😁")
        return
    file_info = getfileid(hello)
    if not file_info:
        await msg.edit("**Not supported!** 🤣")
        return
    file = await hello.download(f'{client.rnd_id()}.mp3')
    r = (await shazam.recognize_song(file)).get('track', None)
    os.remove(file)
    if r is None:
        await msg.edit('**⚠️ Cannot recognize the audio**')
        return
    out = f'**🎵 Song Name** : `{r["title"]}`\n'
    out += f'**🗣️ Artist** : `{r["subtitle"]}`\n'
    buttons = buttons = ([
                [InlineKeyboardButton('🎧 𝗟𝗶𝘀𝘁𝗲𝗻', url=f'{r["url"]}')],
                [InlineKeyboardButton('📲 𝗦𝗵𝗮𝗿𝗲', url=f'{r["share"]["html"]}')]
    ])
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_chat_action("upload_photo")
    await message.reply_photo(
        r['images']['coverarthq'],
        caption=out,
        quote=True
        reply_markup=reply_markup
    )
    await msg.delete()
