from time import time
from pytube import YouTube

def youtube(link: str) -> str:
    pytube = YouTube(link)
    stream = pytube.streams.get_highest_resolution()

    filename = f'temp{round(time() * 1000)}.mp4'

    try:
        stream.download(output_path='temp', filename=filename)
    except:
        return None
    return filename
