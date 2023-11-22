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
    #TODO: VERIFY DOWNLOAD TYPE
    type = request.form['type']

    # Media link
    link = request.form['text']
    
    # TODO: VERIFY LINK FORMAT
    filename = youtube(link, type == 'audio')

    # Verify the filename
    if(filename):
        # Download the file
        return send_file( f'temp/{filename}', as_attachment=True)
    else:
        # Render index again
        return render_template('index.html') # TODO: SHOW POSSIBLE ERRORS

# Scope verification
if __name__ == "__main__":
    # Start the cleaner
    cleaner_thread.start()

    # Start the app
    app.run(debug=True) # TODO: TURN OFF DEBUG MODE

    # Join cleaner before end
    cleaner_thread.join()