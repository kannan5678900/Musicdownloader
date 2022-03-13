from pyrogram import filters
# from pyromod import listen
from bot import bot as Bot
import os
import io
from PIL import Image
from music_tag import load_file

@Bot.on_message(filters.command(["edit"]))
async def tag(bot, message):
    msg = await message.reply("Downloading...")
    hello = message.reply_to_message
    chat_id = message.chat.id
    if not message.reply_to_message:
        return await msg.edit("please reply to some message")
    if not message.reply_to_message.audio:
        return await msg.edit("reply to some audio")
    await hello.download(f"temp/{message.reply_to_message.audio.file_name}.mp3")
    music = load_file(f"temp/{message.reply_to_message.audio.file_name}.mp3")

    try:
        artwork = music['artwork']
        image_data = artwork.value.data
        img = Image.open(io.BytesIO(image_data))
        img.save("temp/artwork.jpg")
    except ValueError:
        image_data = None

    await msg.delete()
    fname = await bot.ask(message.chat.id,'`Send the Filename`', filters=filters.text, parse_mode='Markdown')
    title = await bot.ask(message.chat.id,'`Send the Title name`', filters=filters.text, parse_mode='Markdown')
    artist = await bot.ask(message.chat.id,'`Send the Artist(s) name`', filters=filters.text, parse_mode='Markdown')
    answer = await bot.ask(message.chat.id,'`Send the Artwork or` /skip', filters=filters.photo | filters.text, parse_mode='Markdown')
    music.remove_tag('artist')
    music.remove_tag('title')
    music['artist'] = artist.text
    music['title'] = title.text

    if answer.photo:
        await bot.download_media(message=answer.photo, file_name="temp/artwork.jpg")
        music.remove_tag('artwork')
        with open('temp/artwork.jpg', 'rb') as img_in:
            music['artwork'] = img_in.read()
    music.save()

    try:
        await message.reply_audio(performer=artist.text, title=title.text, duration=message.reply_to_message.audio.duration, audio=f"temp/{message.reply_to_message.audio.file_name}.mp3", thumb='temp/artwork.jpg' if answer.photo or image_data else None)
    except Exception as e:
        print(e)
        return
    os.remove(f"temp/{message.reply_to_message.audio.file_name}.mp3") 
