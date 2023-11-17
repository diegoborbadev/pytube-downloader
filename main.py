from downloader import youtube
from cleaner import clear_directory
from threading import Thread
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

cleaner_thread = Thread(target=clear_directory)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def download():
    link = request.form['text']
    filename = youtube(link)

    if(filename):
        filePath = f'temp/{filename}'
        #TODO: DELETE AFTER SEND
        return send_file(filePath, as_attachment=True)
    else:
        return render_template('index.html')


cleaner_thread.start()
app.run(debug=True) # TODO: TURN OFF DEBUG MODE
cleaner_thread.join()