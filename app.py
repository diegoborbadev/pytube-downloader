from time import time
from pytube import YouTube
from threading import Thread
from urllib.error import URLError
from cleaner import clear_directory
from loggers import error_logger, info_logger
from pytube.exceptions import RegexMatchError, AgeRestrictedError
from flask import Flask, render_template, request, send_file, redirect, url_for

# App instance
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Automatically clean the /temp
cleaner_thread = Thread(target=clear_directory)

# Index
@app.route('/')
def index():
    message = request.args.get('message') or ""
    return render_template('index.html', message=message)

# Get download streams
def get_streams(link: str):
    # Instance pytube
    pytube = YouTube(link)

    # Video Streams
    video_streams = pytube.streams.filter(only_video=True).order_by("resolution").desc()

    # Audio Streams
    audio_streams = pytube.streams.filter(only_audio=True, subtype='mp4').order_by("abr").desc()

    # Return streams
    return video_streams, audio_streams

# Stream select endpoint
@app.route('/streams', methods=['POST'])
def streams():
    # Video link
    link = request.form['link']
    
    try:
        # Get streams
        video_streams, audio_streams = get_streams(link)
        return render_template('streams.html', link=link, video_streams=video_streams, audio_streams=audio_streams)
    
    # Input problem
    except RegexMatchError:
        message = 'Invalid link!'
   
   # Connection Problem
    except URLError:
        error_logger.exception('URLError: Connection problem!')
        message = 'Connection problem!'

    # Age Restricted Video
    except AgeRestrictedError:
        message = 'Age restricted videos cannot be downloaded!'

    return redirect(url_for('index', message=message))
    
    
# Download endpoint (Local)
@app.route('/download', methods=['POST'])
def download():
    # Stream index
    itag = int(request.form['stream'])
    
    # Video link
    link = request.form['link']

    # Get the stream
    stream = YouTube(link).streams.get_by_itag(itag)

    # Generate filename
    filename = f'temp{round(time() * 1000)}.{stream.subtype if stream.type == "video" else "mp3"}'

    # Download
    stream.download(output_path='temp', filename=filename)

    # Redirect
    return render_template('download.html', filename=filename)

# Download endpoint (Browser)
@app.route('/download/<filename>')
def downloadFile(filename):
    # Download the file (browser)
    return send_file( f'temp/{filename}', as_attachment=True) 

# Scope verification
if __name__ == "__main__":
    # Start the cleaner
    cleaner_thread.start()

    # Start the app
    app.run()

    # Join cleaner before end
    cleaner_thread.join()