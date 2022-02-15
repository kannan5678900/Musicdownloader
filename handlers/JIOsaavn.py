import aiohttp
import requests

JIO = "http://starkmusic.herokuapp.com/result/?query={query}"

async def JIO(query: str):
    async with requests.get(JIO) as res:
        return (await res.json())["results"] if ((await res.json()).get("results", None) is not None) else []

