#!/usr/bin/env python
import os, io

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './codesense-43ac4dd2f444.json'

def transcribe_file(speech_file):
    #Transcribe the speech file and returns it as a string
    #File must be .wav, mono 
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()
    
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
         encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
       # sample_rate_hertz=44100,
        language_code='en-US')

    response = client.recognize(config, audio)
    text = ""
    for result in response.results:
        #print('Transcript: {}'.format(result.alternatives[0].transcript))
        text += '{}'.format(result.alternatives[0].transcript)
    return text

filename = "/Users/ecr/Downloads/strange.wav"  
text = transcribe_file(filename)
print(text)
