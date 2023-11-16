import time
from pytube import YouTube

def ytDownload(link: str) -> str:
    pytube = YouTube(link)
    stream = pytube.streams.get_highest_resolution()

    filename = f'temp{round(time.time() * 1000)}.mp4'

    try:
        stream.download(output_path='temp', filename=filename)
    except:
        return None
    return filename
