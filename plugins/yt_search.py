from pyrogram import Client, filters

from youtubesearchpython import SearchVideos

from plugins.google import get_text

async def ytsearch(query, limit):
    result = ""
    videolinks = SearchVideos(query.lower(), limit=limit, offset=1, mode="dict")
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
        return await message.reply_text("`Give me Something to Search in YT!`😇")
    video = await message.reply_text("`Searching...`")
    lim = 10
    try:
        full_response = await ytsearch(query, limit=lim)
    except Exception as e:
        return await message.edit(video, str(e), time=10)
    text = f"**•  Search Query:**\n`{query}`\n\n**•  Results:**\n{full_response}"
    await message.reply_text(text=text)
    await video.delete()
