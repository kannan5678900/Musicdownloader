import aiohttp
import requests

JIO = "http://starkmusic.herokuapp.com/result/?query={}"

async def JIO(query: str):
    async with requests.get(url=JIO(query)) as res:
        return (await res.json())["results"] if ((await res.json()).get("results", None) is not None) else []

