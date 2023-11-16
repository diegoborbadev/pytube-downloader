from flask import Flask, render_template, request, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def download():
    link = request.form['text']
    return send_file('test.txt', as_attachment=True)

#TODO: TURN OFF DEBUG MODE
app.run(debug=True);