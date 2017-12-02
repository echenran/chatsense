from flask import Flask, flash, redirect, request
import json
from processaudioapp import processaudio
app = Flask(__name__)

@app.route('/send', methods=['GET', 'POST'])
def process_send():
    print "[Request headers]:", request.headers
    print "[Request data]:", len(request.data)
    print "[Request form]:", request.form
    
    if request.data:
        res = processaudio.analyze(request.data)

    return "Received\nProcessed:",res

@app.route('/getback', methods=['GET', 'POST'])
def process_getback():
    print "[Request headers]:", request.headers
    print "[Request data]:", len(request.data)
    print "[Request form]:", request.form
    
    if request.data:
        print "[Request data keys]:", request.data.keys()

    return "Not done yet\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
