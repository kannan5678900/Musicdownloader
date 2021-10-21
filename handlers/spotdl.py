import os
import ffmpeg
import subprocess
from typing import List
from pyrogram.types import Message

def download_from_spotify(download_path: str, link: List[str]):

    os.mkdir(download_path)
    os.chdir(download_path)
    os.system(f'spotdl {link}')
    os.chdir("..")

def send_songs_from_directory(
    directory_path: str, client, message: Message):
    directory = os.listdir(directory_path)
    chat_id = message.chat.id
    caption = f"**Uploaded By : @MusicDownloadv2bot**"
    for file in directory:
        if not file.endswith(".mp3"):
            continue
        results = client.send_audio(chat_id,caption=caption,audio=open(f'{directory_path}/{file}', 'rb'))
    subprocess.run(['rm', '-r', directory_path])