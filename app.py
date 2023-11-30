from downloader import download
from cleaner import clear_directory
from threading import Thread
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

# Download endpoint
@app.route('/', methods=['POST'])
def download():
    #TODO: VERIFY DOWNLOAD TYPE PROPPERLY
    type = request.form['type']

    # Media link
    link = request.form['text']
    
    try:
        # Get the file (locally)
        filename = download(link, type == 'audio')
        
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