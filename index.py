from flask import Flask, flash, redirect, request
import json, re
from processaudio import ProcessAudio
import time
app = Flask(__name__)

""" Get one-message preview of a conversation """
@app.route('/getconvoprev', methods=['GET', 'POST'])
def process_getconvoprev():
    print request.form
    user1 = request.form['user1']
    user2 = request.form['user2']
    howmany = request.form['num_msgs']
    
    convo = open("convo.json", 'r')
    msgs = convo.read()

    return str(msgs)

""" Get the last 20 messages of a conversation """
@app.route('/getconvomsgs', methods=['GET', 'POST'])
def process_getconvomsgs():
    print request.form
    user1 = request.form['user1']
    user2 = request.form['user2']
    howmany = request.form['num_msgs']
    
    convo = open("convo.json", 'r')
    msgs = convo.read()

    return str(msgs)

@app.route('/send', methods=['GET', 'POST'])
def process_send():
    print "[Request headers]:", request.headers
    print "[Request data]:", len(request.data)
    print "[Request form]:", request.form

    datestr = time.strftime("%m/%d", time.localtime())
    timestr = time.strftime("%I:%M", time.localtime())
    
    if request.data:
        AUDIOFILE = "transmittedaudio.wav"

        print "Got data back!"
        f = open(AUDIOFILE, "w")
        f.write(request.data)
        print "Wrote data!"
        f.close()

        lines = open(AUDIOFILE, "r").readlines()
        if re.match('RIFF.*WAVE', lines[0]): # It is a wave file
            originalname = AUDIOFILE
        else: # It is a PCM file
            #print "line[0]: {}".format(lines[0])
            #metadata = lines[0]
            #try:
            #    originalname = re.search('[\w]+\.[a-zA-Z]+', metadata).group(0)
            #    print "  filename inside line[0]: {}".format(originalname)
            #except:
            #    originalname = ""
            #    print "  no valid filename found"
            #    
            #lines[0] = ""
            #f = open(AUDIOFILE, 'w')
            #for line in lines:
            #    f.write(line)
            #f.close()
            originalname = AUDIOFILE
            pass

        # Here's where the magic happens
        pa = ProcessAudio()
        pa.load(AUDIOFILE, originalname)
        res = pa.report()
        
        # Format emotions data
        for key in res["emotions"].keys():
            print "rounding {}={}".format(key, res['emotions'][key])
            res['emotions'][key] = int(round(res['emotions'][key]*100))

        # Add time and date
        res['datestr'] = datestr
        res['timestr'] = timestr

        return str(res)
    
    return "File was not successfully sent"

@app.route('/getback', methods=['GET', 'POST'])
def process_getback():
    print "[Request headers]:", request.headers
    print "[Request data]:", len(request.data)
    print "[Request form]:", request.form
    
    if request.data:
        print "[Request data]:", request.data

    return "Not done yet\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
