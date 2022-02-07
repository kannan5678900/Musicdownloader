import datetime
import html
import bs4
import requests
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters, Client

from plugins.google import get_text

def shorten(description, info='anilist.co'):
    msg = ""
    if len(description) > 700:
        description = description[0:500] + '....'
        msg += f"\n<b>Description</b>: <i>{description}</i>[Read More]({info})"
    else:
        msg += f"\n<b>Description</b>:<i>{description}</i>"
    return msg

anime_query = '''
   query ($id: Int,$search: String) { 
      Media (id: $id, type: ANIME,search: $search) { 
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          episodes
          season
          type
          format
          status
          duration
          siteUrl
          studios{
              nodes{
                   name
              }
          }
          trailer{
               id
               site 
               thumbnail
          }
          averageScore
          genres
          bannerImage
      }
    }
'''

url = 'https://graphql.anilist.co'

@Client.on_message(filters.command(['anime']))
async def anime(client, message): 
    hi = await message.reply("🔎")
    chat_id = message.chat.id
    user_id = message.from_user.id
    search = get_text(message)
    print(f"Anime:{search}.UserId: {user_id}")
    if not search:
        await hi.edit("`Give me any Anime name to Search.😊`\n\n`/anime Avengers`")
        return
    else:
        search = search[1]
    variables = {"search": search}
    json = (
        requests.post(url, json={"query": anime_query, "variables": variables})
        .json()["data"]
        .get("Media", None)
    )
    if json:
        msg = f"<b>{json['title']['romaji']}</b>(<code>{json['title']['native']}</code>)\n<b>Type</b>: {json['format']}\n<b>Status</b>: {json['status']}\n<b>Episodes</b>: {json.get('episodes', 'N/A')}\n<b>Duration</b>: {json.get('duration', 'N/A')} Per Ep.\n<b>Score</b>: {json['averageScore']}\n<b>Genres</b>: <code>"
        for x in json["genres"]:
            msg += f"{x}, "
        msg = msg[:-2] + "</code>\n"
        msg += "<b>Studios</b>: <code>"
        for x in json["studios"]["nodes"]:
            msg += f"{x['name']}, "
        msg = msg[:-2] + "</code>\n"
        info = json.get("siteUrl")
        trailer = json.get("trailer", None)
        if trailer:
            trailer_id = trailer.get("id", None)
            site = trailer.get("site", None)
            if site == "youtube":
                trailer = "https://youtu.be/" + trailer_id
        description = (
            json.get("description", "N/A")
            .replace("<i>", "")
            .replace("</i>", "")
            .replace("<br>", "")
        )
        msg += shorten(description, info)
        image = info.replace("anilist.co/anime/", "img.anili.st/media/")
        if trailer:
            buttons = [
                [
                    InlineKeyboardButton("More Info", url=info),
                    InlineKeyboardButton("Trailer 🎬", url=trailer),
                ],
            ]
        else:
            buttons = [[InlineKeyboardButton("More Info", url=info)]]
        if image:
            try:
                await client.send_chat_action(chat_id, "upload_photo")
                await message.reply_photo(photo=image, caption=msg, reply_markup=InlineKeyboardMarkup(buttons), quote=True)
                await hi.delete(hi)
            except:
                msg += f" [〽️]({image})"
                await message.reply(msg)
                await hi.delete(hi)
        else:
            await message.reply(msg)
            await hi.delete(hi)
