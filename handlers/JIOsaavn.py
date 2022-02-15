import aiohttp
from requests.utils import requote_uri

JIO = "http://starkmusic.herokuapp.com/result/?query={}"

async def JIO(query: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(requote_uri(JIO.format(query))) as res:
            return (await res.json())["results"] if ((await res.json()).get("results", None) is not None) else []

