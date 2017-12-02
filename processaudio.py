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

import sys, os
import scipy.io.wavfile

# Constants
vokaturi = "./vokaturi"
audiotranscodelib = "./python-audiotranscode"
WAV = "wav"

# Load Vokaturi
sys.path.append(vokaturi + "/api")
import Vokaturi
print ("Loading Vokaturi...")
Vokaturi.load(vokaturi + "/lib/Vokaturi_mac.so")

# Load audiotranscode
sys.path.append(audiotranscodelib)
import audiotranscode
print ("Loading audiotranscode...")
at = audiotranscode.AudioTranscode()

# Load + convert audio
oldfilename = newfilename = sys.argv[1]
print ("Loading sound file <{}>...".format(oldfilename))
if oldfilename.split(".")[1].lower() != WAV:
    print ("Converting sound file from .{} to .{}...".format(oldfilename.split(".")[1], WAV))
    newfilename = oldfilename.split(".")[0] + "." + WAV
    at.transcode(oldfilename, newfilename)
    print("oldfilename: {} newfilename: {} ({} bytes)".format(oldfilename, newfilename, os.path.getsize("./"+newfilename)))

# Read audio
print ("Reading sound file...")
(sample_rate, samples) = scipy.io.wavfile.read(newfilename)
print ("   sample rate %.3f Hz" % sample_rate)

print ("Allocating Vokaturi sample array...")
buffer_length = len(samples)
print ("   %d samples, %d channels" % (buffer_length, samples.ndim))
c_buffer = Vokaturi.SampleArrayC(buffer_length)
if samples.ndim == 1:  # mono
	c_buffer[:] = samples[:] / 32768.0
else:  # stereo
	c_buffer[:] = 0.5*(samples[:,0]+0.0+samples[:,1]) / 32768.0

print ("Creating VokaturiVoice...")
print("size of {}: {} bytes".format(newfilename, os.path.getsize(newfilename)))
voice = Vokaturi.Voice (sample_rate, buffer_length)

print ("Filling VokaturiVoice with samples...")
print("size of {}: {} bytes".format(newfilename, os.path.getsize(newfilename)))
voice.fill(buffer_length, c_buffer)

print ("Extracting emotions from VokaturiVoice...")
quality = Vokaturi.Quality()
emotionProbabilities = Vokaturi.EmotionProbabilities()
voice.extract(quality, emotionProbabilities)

if quality.valid:
	print ("Neutral: %.3f" % emotionProbabilities.neutrality)
	print ("Happy: %.3f" % emotionProbabilities.happiness)
	print ("Sad: %.3f" % emotionProbabilities.sadness)
	print ("Angry: %.3f" % emotionProbabilities.anger)
	print ("Fear: %.3f" % emotionProbabilities.fear)
else:
	print ("Not enough sonorancy to determine emotions")

voice.destroy()
