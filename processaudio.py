#!/usr/bin/env python

# measure_wav_mac.py
# Paul Boersma 2017-09-17
#
# A sample script that uses the Vokaturi library to extract the emotions from
# a wav file on disk. The file has to contain a mono recording.
#
# Call syntax:
#   python3 measure_wav_mac.py path_to_sound_file.wav
#
# For the sound file hello.wav that comes with OpenVokaturi, the result should be:
#   Neutral: 0.760
#   Happy: 0.000
#   Sad: 0.238
#   Angry: 0.001
#   Fear: 0.000
from flask import Blueprint
import sys, os
import scipy.io.wavfile
from pydub import AudioSegment

# Constants
WAV = "wav"
VOKATURI = "./vokaturi"
AUDIOTRANSCODELIB = "./python-audiotranscode"

class ProcessAudio(object):

    # Load libraries
    sys.path.append(VOKATURI + "/api")
    import Vokaturi as vokaturilib
    vok = vokaturilib
    sys.path.append(AUDIOTRANSCODELIB)
    import audiotranscode as audiotranscodelib
    audtrans = audiotranscodelib

    def __init__(self):
        # Load Vokaturi
        print ("Loading Vokaturi...")
        self.vok.load(VOKATURI + "/lib/Vokaturi_mac.so")

        # Load audiotranscode
        print ("Loading audiotranscode...")
        self.at = self.audtrans.AudioTranscode()

        self.filename = None

    def load(self, filepath):
        # Load + convert audio
        """oldfilename = newfilename = filepath.split("/")[-1]
        print ("Loading sound file <{}>...".format(oldfilename))
        if oldfilename.split(".")[-1].lower() != WAV:
            print ("Converting sound file from .{} to .{}...".format(oldfilename.split(".")[-1], WAV))
            newfilename = oldfilename.split(".")[0] + "." + WAV
            self.at.transcode(filepath, newfilename)
            self.filename = newfilename

            print("oldfilename: {} newfilename: {} ({} bytes)".format(oldfilename, newfilename, os.path.getsize("./"+newfilename)))
        else:
            self.filename = filepath"""
        oldfilename = newfilename = filepath.split("/")[-1]
        print ("Loading sound file <{}>...".format(oldfilename))
        if oldfilename.split(".")[-1].lower() != WAV:
            print ("Converting sound file from .{} to .{}...".format(oldfilename.split(".")[-1], WAV))
            newfilename = oldfilename.split(".")[0] + "." + WAV
            old = AudioSegment.from_mp3(filepath)
            old.export(newfilename, format=WAV)
            self.filename = newfilename

            print("oldfilename: {} newfilename: {} ({} bytes)".format(oldfilename, newfilename, os.path.getsize("./"+newfilename)))
        else:
            self.filename = filepath


    def analyze(self):
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

obj = ProcessAudio()
#f = "./vokaturi/examples/hey-sweetness.wav"
f = "../../Downloads/hurtme.mp3"
obj.load(f)
print(obj.analyze())
