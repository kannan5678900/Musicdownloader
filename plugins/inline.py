from pyrogram import types, filters
from bot import bot
# from handlers.JIOsaavn import *
import re
import urllib
import requests
from pyrogram import Client, errors
from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from youtubesearchpython import SearchVideos


@bot.on_inline_query()
async def inline_func(client, query):
    string = query.query.lower()
    answers = []
    if string == '':
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text='Need help? Click here',
            switch_pm_parameter='help_inline',
        )
        return
    if string.split()[0] == 'related':
        if len(string.split()) == 1:
            await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text='Input Song ID',
                switch_pm_parameter='help_inline',
            )
            return
        try:
            track_id = int(string.split(None, 1)[1])
        except ValueError:
            return
        try:
            for x in (await bot.related(track_id)):
                try:
                    result = (
                        x['images']['coverarthq'],
                        x['images']['coverart'],
                        x['title'], x['subtitle'],
                        x['share']['href'],
                        x['share']['html']
                    )
                except KeyError:
                    result = (
                        None,
                        None,
                        x['title'],
                        x['subtitle'],
                        x['share']['href'],
                        x['share']['html']
                    )
                image, thumb, title, artist, link, share = result
                answers.append(
                    types.InlineQueryResultArticle(
                        title=title,
                        description=artist,
                        thumb_url=thumb,
                        input_message_content=types.InputTextMessageContent(
                            f'**Title**: {title}\n**Artist**: {artist}[\u200c\u200c\u200e]({image})'
                        ),
                        reply_markup=types.InlineKeyboardMarkup(
                            [
                                [
                                    types.InlineKeyboardButton(
                                        '🔗 Share',
                                        url=f'{share}'
                                    )
                                ],
                                [
                                    types.InlineKeyboardButton(
                                        '🎵 Listen',
                                        url=f'{link}'
                                    )
                                ]
                            ]
                        )
                    )
                )
        except TypeError:
            return await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text='cannot find the Song',
                switch_pm_parameter='help_inline',
            )
            return
    elif string.split()[0] == 'artist':
        if len(string.split()) == 1:
            await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text='Input Artist Name',
                switch_pm_parameter='help_inline',
            )
            return
        artists = await bot.get_artist(string.split(None, 1)[1])
        if artists is None:
            return await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text='Cannot find the Artist',
                switch_pm_parameter='help_inline',
            )
            return
        for artist in artists:
            answers.append(
                types.InlineQueryResultArticle(
                        title=artist.name,
                        description=None,
                        thumb_url=artist.avatar or None,
                        input_message_content=types.InputTextMessageContent(
                            f'**Artist name:**{artist.name} [\u200c\u200c\u200e]({artist.avatar})'
                        ),
                        reply_markup=types.InlineKeyboardMarkup(
                            [
                                [
                                    types.InlineKeyboardButton(
                                        '🔗 More Info',
                                        url=f'{artist.url}'
                                    )
                                ]
                            ]
                        )
                    ) 
                )
    elif string.split()[0] == 'tracks':
        if len(string.split()) == 1:
            await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text='Input Artist ID',
                switch_pm_parameter='help_inline',
            )
            return
        tracks = await bot.get_artist_tracks(string.split(None, 1)[1])
        if tracks is None:
            return await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text='Cannot find the Artist',
                switch_pm_parameter='help_inline',
            )
            return
        for track in tracks:
            answers.append(
                types.InlineQueryResultArticle(
                        title=track.title,
                        description=track.subtitle,
                        thumb_url=track.apple_music_url or None,
                        input_message_content=types.InputTextMessageContent(
                            f'**Title:** {track.title}\n**Artist**: {track.subtitle} [\u200c\u200c\u200e]({track.apple_music_url})'
                        ),
                        reply_markup=types.InlineKeyboardMarkup(
                            [
                                [
                                    types.InlineKeyboardButton(
                                        '🎵 Listen',
                                        url=f'{track.shazam_url}'
                                    )
                                ]
                            ]
                        )
                    ) 
                )
    
    elif string.split()[0] == "yt":
        if len(string.split()) == 1:
            await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text="Type a YouTube video Name...",
                switch_pm_parameter="help",
                cache_time=0
            )
            return
        starkisnub = urllib.parse.quote_plus(string)
        search = SearchVideos(string.split(None, 1)[1], max_results=50, offset=1, mode="dict")
        mi = search.result()
        moi = mi["search_result"]

        for mio in moi:
            mo = mio["link"]
            thum = mio["title"]
            fridayz = mio["id"]
            thums = mio["channel"]
            td = mio["duration"]
            tw = mio["views"]
            kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
            okayz = f"{mo}"
            hmmkek = f'Channel : {thums} \nDuration : {td} \nViews : {tw}'
            answers.append(
                InlineQueryResultArticle(
                    title=thum,
                    description=hmmkek,
                    input_message_content=InputTextMessageContent(
                      message_text=okayz)
              )
        )
        try:
            await query.answer(
                results=answers,
                cache_time=0
            )
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text="Error: Search timed out",
                switch_pm_parameter="",
            )

    elif string.split()[0] == "sg":
        if len(string.split()) == 1:
            await client.answer_inline_query(
                query.id,
                results=answers,
                switch_pm_text="Type a song name...",
                switch_pm_parameter="about",
                cache_time=0
            )
            return
        query = urllib.parse.quote_plus(string)
        hel = string.split(" ", 1)[-1]
        song = f"http://starkmusic.herokuapp.com/result/?query=First_Class"
        hi = requests.get(url=song).json()
        for me in hi:
            title = me['song']
            singer = me['singers']
            dur = me['duration']
            lang = me['language']
            caption = f"Singer : {singer} \nDuration : {dur} \nLanguage = {lang}"
            xxx = f'/saavn {title}'
            answers.append(
                InlineQueryResultArticle(
                    title=title,
                    description=caption,
                    input_message_content=InputTextMessageContent(
                      message_text=xxx)
              )
         )


@Client.on_inline_query()
async def inline(bot, query):

          searche = query.query
          if searche.startswith("1"):
                await JIO(bot, query, searche)
