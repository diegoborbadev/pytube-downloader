from time import time
from pytube import YouTube
from threading import Thread
from urllib.error import URLError
from cleaner import clear_directory
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
    streams = pytube.streams.filter(type='video', progressive="False").order_by("resolution").desc()

    # Audio Streams
    streams.fmt_streams+= pytube.streams.filter(type='audio', progressive=None).order_by("abr").desc()

    # Return streams
    return streams

# Stream select endpoint
@app.route('/streams', methods=['POST'])
def streams():
    # Video link
    link = request.form['link']
    
    try:
        # Get streams
        streams = get_streams(link)
        return render_template('streams.html', link=link, streams=streams)
    
    # Input problem
    except RegexMatchError:
        message = 'Invalid link!'
   
   # Connection Problem
    except URLError:
        message = 'Connection problem!'

    # Age Restricted Video
    except AgeRestrictedError:
        message = 'Age restricted videos cannot be downloaded!'

    return redirect(url_for('index', message=message))
    
    
# Download endpoint (Local)
@app.route('/download', methods=['POST'])
def download():
    # Stream index
    index = int(request.form['stream'])
    
    # Video link
    link = request.form['link']

    # Get the stream
    stream = get_streams(link)[index]

    # Generate filename
    filename = f'temp{round(time() * 1000)}.{stream.subtype}'

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
    app.run(debug=True) # TODO: TURN OFF DEBUG MODE

    # Join cleaner before end
    cleaner_thread.join()