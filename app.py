from downloader import youtube
from cleaner import clear_directory
from threading import Thread
from flask import Flask, render_template, request, send_file

# App instance
app = Flask(__name__)

# Automatically clean the /temp
cleaner_thread = Thread(target=clear_directory)

# Index
@app.route('/')
def index():
    return render_template('index.html')

# Download endpoint
@app.route('/', methods=['POST'])
def download():
    # Media link
    link = request.form['text']
    filename = youtube(link)

    # Verify the filename
    if(filename):
        # Download the file
        return send_file( f'temp/{filename}', as_attachment=True)
    else:
        # Render index again
        return render_template('index.html') # TODO: Show possible erros

# Start the cleaner
cleaner_thread.start()

# Start the app
app.run(debug=True) # TODO: TURN OFF DEBUG MODE

# Join cleaner before end
cleaner_thread.join()