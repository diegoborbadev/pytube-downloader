from time import time
from pytube import YouTube
from threading import Thread
from cleaner import clear_directory
from flask import Flask, render_template, request, send_file

# App instance
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Automatically clean the /temp
cleaner_thread = Thread(target=clear_directory)

# Index
@app.route('/')
def index():
    return render_template('index.html')

# Get download streams
def get_streams(link: str, type : str):
    # Instance pytube
    pytube = YouTube(link)

    # Verify type
    is_audio = type == 'audio'
    progressive=None if is_audio else "False"
    order_by = "abr" if is_audio else "resolution"

    # Return streams
    return pytube.streams.filter(type=type, progressive=progressive).order_by(order_by).desc()

# Stream select endpoint
@app.route('/streams', methods=['POST'])
def streams():
    # Download type
    type = request.form['type']
    
    # Video link
    link = request.form['link']
    
    # Get streams
    streams = get_streams(link, type)

    return render_template('streams.html', link=link, streams=streams, type=type)
    
    
# Download endpoint
@app.route('/download', methods=['POST'])
def download():
    # Stream id (itag)
    stream_id = request.form['stream']
    
    # Video link
    link = request.form['link']

    # Download type
    type = request.form['type']

    # Get the stream
    stream = get_streams(link, type).get_by_itag(int(stream_id))

    # Generate filename
    filename = f'temp{round(time() * 1000)}.{stream.subtype}'

    # Download
    try:
        stream.download(output_path='temp', filename=filename)
        # Download the file (browser)
        return send_file( f'temp/{filename}', as_attachment=True)
    except:
        # Render index again (with error)
        return render_template('index.html', error='Invalid link')   

# Scope verification
if __name__ == "__main__":
    # Start the cleaner
    cleaner_thread.start()

    # Start the app
    app.run(debug=True) # TODO: TURN OFF DEBUG MODE

    # Join cleaner before end
    cleaner_thread.join()