from flask import Flask, flash, redirect, session, abort, render_template, request
import json
app = Flask(__name__)

@app.route('/send', methods=['GET', 'POST'])
def process_send():
    print "[Request headers]:", request.headers
    print "[Request data]:", len(request.data)
    print "[Request form]:", request.form
    return "Received\n"

@app.route('/getback', methods=['GET', 'POST'])
def process_getback():
    print "[Request headers]:", request.headers
    print "[Request data]:", len(request.data)
    print "[Request form]:", request.form
    return "Not done yet\n"
