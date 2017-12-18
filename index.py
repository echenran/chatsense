from flask import Flask, flash, redirect, request
import json
from processaudio import ProcessAudio
import time
app = Flask(__name__)

@app.route('/send', methods=['GET', 'POST'])
def process_send():
    print "[Request headers]:", request.headers
    print "[Request data]:", len(request.data)
    print "[Request form]:", request.form

    datestr = time.strftime("%m/%d", time.localtime())
    timestr = time.strftime("%I:%M", time.localtime())
    
    if request.data:
        AUDIOFILE = "transmittedaudio.pcm"

        print "Got data back!"
        f = open(AUDIOFILE, "w")
        f.write(request.data)
        print "Wrote data!"
        f.close()

        lines = open(AUDIOFILE, "r").readlines()

        # Here's where the magic happens
        pa = ProcessAudio()
        pa.load(AUDIOFILE)
        res = pa.report()
        print "Got report:", res
        
        # Format emotions data
        for key in res["emotions"].keys():
            res['emotions'][key] = int(round(res['emotions'][key]*100))

        # Add time and date
        res['datestr'] = datestr
        res['timestr'] = timestr

        return str(res)
    
    return "File was not successfully sent"

""" Get the previously sent messages in the conversation """
@app.route('/getconvomsgs', methods=['GET', 'POST'])
def process_getconvomsgs():
    print request.form
    
    convo = open("convo.json", 'r')
    msgs = convo.read()

    return str(msgs)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
