# Chatsense
Chatsense is an Android messaging app geared towards the autistic community
that executes speech-to-text transcription, performs real-time audial sentiment
analysis, and displays messages in the color of the emotion of the sender’s
voice with an emoji corresponding to the sender’s dominant emotion.

### Technical Details
- Frontend: Java (Android Studio)
- Server: Flask app on a PythonAnywhere instance, Google Cloud API, Vokaturi
- Middleware: Java

Once a user speaks their message into the phone, Chatsense sends the audio clip
to the PythonAnywhere server, which processes it by:

- stripping the text out from the audio (Google Cloud Speech)
- analyzing the emotion in the speaker's tone (Vokaturi)
- synthesizing the breakdown of the speaker's emotion and creating a unique
color for the message

Then, all this information is sent back to the client, which algorithmically
determines what emoji the message is to be accompanied by and sends the message
in the color of the speaker's tone with the accompanying emoji.

### Fun Facts
This project was created within the span of a weekend at YHack 2017 and won the
Mirum & JWT _Can a Computer Hear How You Feel?_ sponsor prize. Check out our
[Devpost](https://devpost.com/software/chatsense)! This project is ongoing.
