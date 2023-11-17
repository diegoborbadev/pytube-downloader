from time import time
from pytube import YouTube

def youtube(link: str) -> str:
    """Donwload a video from youtube

    #### Parameters
    link : str
        Video link
    """

    # Instance pytube
    pytube = YouTube(link)

    # Get the stream
    stream = pytube.streams.get_highest_resolution()

    # Generate filename
    filename = f'temp{round(time() * 1000)}.mp4'

    # Download
    try:
        stream.download(output_path='temp', filename=filename)
        return filename
    except:
        return None