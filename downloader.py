from time import time
from pytube import YouTube

def download(link: str, audio = False) -> str:
    """Donwload a video from youtube

    #### Parameters
    link : str
        Video link
    """

    # Instance pytube
    pytube = YouTube(link)

    # Get the stream
    stream = pytube.streams.get_audio_only() if audio else pytube.streams.get_highest_resolution()

    # Generate filename
    filename = f'temp{round(time() * 1000)}.{"mp3" if audio else "mp4"}'

    # Download
    try:
        stream.download(output_path='temp', filename=filename)
        return filename
    except:
        return None