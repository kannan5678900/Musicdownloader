from pyrogram import Client, filters
from youtubesearchpython import VideosSearch

from plugins.google import get_text
from plugins.shazam import edit_or_reply

async def ytsearch(query, limit):
    result = ""
    videolinks = VideosSearch(query.lower(), limit=limit)
    for v in videolinks.result()["result"]:
        textresult = f"[{v['title']}](https://www.youtube.com/watch?v={v['id']})\n"
        try:
            textresult += f"**Description : **`{v['descriptionSnippet'][-1]['text']}`\n"
        except Exception:
            textresult += "**Description : **`None`\n"
        textresult += f"**Duration : **__{v['duration']}__  **Views : **__{v['viewCount']['short']}__\n"
        result += f"☞ {textresult}\n"
    return result

@Client.on_message(filters.command(["yts"]))
async def yt_search(client, message):
    query = get_text(message)
    if not query:
        return await message.reply_text("`Reply to a message or pass a query to search!`")
    video = await message.reply_text("`Searching...`")
    lim = 8
    try:
        full_response = await ytsearch(query, limit=lim)
    except Exception as e:
        return await edit_delete(video_q, str(e), time=10, parse_mode=_format.parse_pre)
    text = f"**•  Search Query:**\n`{query}`\n\n**•  Results:**\n{full_response}"
    await message.reply_text(text=text)
    await video.delete()
