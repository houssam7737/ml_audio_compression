import io
import os
import requests

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import subprocess

# Instantiates a client
client = speech.SpeechClient()

# The name of the audio file to transcribe
file_name = os.path.join(
    os.path.dirname(__file__),
    '0ea0e2f4_nohash_1_2.mp3')

subprocess.call(['ffmpeg', '-i', file_name, 'file.wav'])

# Loads the audio into memory
with io.open('file.wav', 'rb') as audio_file:
    content = audio_file.read()
    audio = types.RecognitionAudio(content=content)

config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    model="command_and_search",
    language_code='en-US')
# import base64

# URL = "https://speech.googleapis.com/v1/speech:recognize?key=AIzaSyDlDWRurKJ4TQ2OThGHfqoA7LkLes3VaBI"

# PARAMS = {
# 	"config": {
# 	    "enableAutomaticPunctuation": "true",
# 	    "encoding": "LINEAR16",
# 	    "languageCode": "en-US",
# 	    "model": "default"
# },
# 	"audio": {
# 	   "content": base64.b64encode(content)
# }
# }

# import json

# with open('request.json', 'w') as fp:
#     json.dump(PARAMS, fp)

# r = requests.post(url= URL, data= PARAMS)

# print(r.text)

# Detects speech in the audio file
response = client.recognize(config, audio)
print(response)

for result in response.results:
    print('Transcript: {}'.format(result.alternatives[0].transcript))
