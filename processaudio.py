#!/usr/bin/env python

import sys, os, wave, io
import scipy.io.wavfile
from pydub import AudioSegment

# Constants
WAV = "wav"
MP3 = "mp3"
PCM = "pcm"
VOKATURI = "./vokaturi"

class ProcessAudio(object):

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './codesense-43ac4dd2f444.json'

    # Load libraries
    print ("Loading Vokaturi...")
    sys.path.append(VOKATURI + "/api")
    import Vokaturi as vokaturilib
    vok = vokaturilib

    def __init__(self):
        # Load Vokaturi
        self.vok.load(VOKATURI + "/lib/Vokaturi_mac.so")

        self.filename = None

    def load(self, audiofile, originalname):
        # Load + convert audio
        print ("Loading sound file <{}>...".format(originalname))
	name = originalname.split(".")[0]
	ext = originalname.split(".")[-1].lower()

        if ext == MP3:
            newfilename = name + ".wav"
            old = AudioSegment.from_mp3(audiofile)
            old.export(newfilename, format=WAV)
            self.filename = newfilename
        elif ext == PCM:
            print "This is a PCM file!"
	    pcmfile = open(audiofile, 'rb')
	    pcmdata = pcmfile.read()
	    pcmfile.close()

	    wavfile = wave.open(name+'.wav', 'wb')
	    wavfile.setparams((1, 2, 44100, 16, 'NONE', 'NONE'))
	    wavfile.writeframes(pcmdata)
	    wavfile.close()
	    self.filename = name+".wav"
        else:
            self.filename = audiofile

    def analyze_emotion(self):
        # Read audio
        print ("Reading sound file...")
        (sample_rate, samples) = scipy.io.wavfile.read(self.filename)
        print ("   sample rate %.3f Hz" % sample_rate)

        print ("Allocating Vokaturi sample array...")
        buffer_length = len(samples)
        print ("   %d samples, %d channels" % (buffer_length, samples.ndim))
        c_buffer = self.vok.SampleArrayC(buffer_length)
        if samples.ndim == 1:  # mono
            c_buffer[:] = samples[:] / 32768.0
        else:  # stereo
            c_buffer[:] = 0.5*(samples[:,0]+0.0+samples[:,1]) / 32768.0

        print ("Creating VokaturiVoice...")
        print("size of {}: {} bytes".format(self.filename, os.path.getsize(self.filename)))
        voice = self.vok.Voice (sample_rate, buffer_length)

        print ("Filling VokaturiVoice with samples...")
        print("size of {}: {} bytes".format(self.filename, os.path.getsize(self.filename)))
        voice.fill(buffer_length, c_buffer)

        print ("Extracting emotions from VokaturiVoice...")
        quality = self.vok.Quality()
        emotionProbabilities = self.vok.EmotionProbabilities()
        voice.extract(quality, emotionProbabilities)

        res = {}
        if quality.valid:
            res['neutrality'] = emotionProbabilities.neutrality
            res['happiness']  = emotionProbabilities.happiness
            res['sadness']    = emotionProbabilities.sadness
            res['anger']      = emotionProbabilities.anger
            res['fear']       = emotionProbabilities.fear
        else:
            print ("Not enough sonorancy to determine emotions")

        voice.destroy()

        return res

    def analyze_text(self):
        """ Transcribe the speech file and returns it as a string;can only be 
        called after calling self.load(); file must be .wav, mono """
        from google.cloud import speech
        from google.cloud.speech import enums
        from google.cloud.speech import types
        client = speech.SpeechClient()
        
        with io.open(self.filename, 'rb') as audio_file:
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

    def report(self):
        """ Returns an object with the text spoken and the emotions in
        the speaker's tone """
        res = {
            "text": self.analyze_text(),
            "emotions": self.analyze_emotion()
        }

        return res
