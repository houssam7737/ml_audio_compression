import io
import os
import requests
import json 

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import subprocess

labels = ["bed", "bird", "cat", "dog", "down", "eight", "five", "four", "go", "happy", "house", "left", "marvin", "nine", "no", "off", "on", "one", "stop", "up", "wow", "yes", "three", "tree"]

transformations = ["0", "2", "4", "8", "16"]
# Instantiates a client
client = speech.SpeechClient()

# The name of the audio file to transcribe
# file_name = os.path.join(
#     os.path.dirname(__file__),
#     '0ea0e2f4_nohash_1_2.mp3')

# labels = ["bed"]
# transformations = ["0"]

accuracies = {}

for label in labels:
    accuracies[label] = {}
    for transformation in transformations:
        directory_name = label + '_transformed_' + transformation
        if transformation == "2":
            directory_name = label + "_transformed"
        if transformation == "0":
            directory_name = label 
        n_files = 0
        n_files_correctly_labelled = 0
        for filename in os.listdir("train/audio/"+directory_name):
            file_path = os.path.join("train/audio/"+directory_name, filename)
            if transformation != "0":
                subprocess.call(['ffmpeg', '-y', '-i', file_path, 'file.wav'])

                # Loads the audio into memory
                with io.open('file.wav', 'rb') as audio_file:
                    content = audio_file.read()
                    audio = types.RecognitionAudio(content=content)
            else:
                # Loads the audio into memory
                with io.open(file_path, 'rb') as audio_file:
                    content = audio_file.read()
                    audio = types.RecognitionAudio(content=content) 

            config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                model="command_and_search",
                language_code='en-US')

            # Detects speech in the audio file
            response = client.recognize(config, audio)

            # print("RESPONSE:\n", response)
            if response.results:
                if response.results[0].alternatives[0].transcript == label:
                    n_files_correctly_labelled += 1
            # else:
            #     continue

            n_files += 1
            for result in response.results:
                print('Transcript: {}'.format(result.alternatives[0].transcript))
            if n_files > 100:
                break
        accuracies[label][transformation] = n_files_correctly_labelled/n_files

with open('accuracies.json', 'w') as fp:
    json.dump(accuracies, fp)

print(accuracies)