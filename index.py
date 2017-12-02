from flask import Flask, flash, redirect, request
import json
from processaudio import ProcessAudio
app = Flask(__name__)

@app.route('/send', methods=['GET', 'POST'])
def process_send():
    print "[Request headers]:", request.headers
    print "[Request data]:", len(request.data)
    print "[Request form]:", request.form
    
    if request.data:
        AUDIOFILE = "transmittedaudio.wav"

        print "Got data back!"
        f = open(AUDIOFILE, "w")
        f.write(request.data)
        print "Wrote data!"
        f.close()
        lines = open(AUDIOFILE, "r").readlines()
        print "line[0]: {}".format(lines[0])
        lines[0] = ""
        print "delet'd"
        print "line[0]: {}".format(lines[0])
        f = open(AUDIOFILE, 'w')
        for line in lines:
            f.write(line)

        f.close()
        print "Closed file!"
        pa = ProcessAudio()
        pa.load(AUDIOFILE)
        res = pa.analyze()

    return str(res)

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
