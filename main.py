import os
import subprocess
from time import sleep
import time
from googletrans import Translator
import pygame
from voicevox import Client
import asyncio
import win32com.client
import speech_recognition as sr
from play import Playing


def speak(text, lang):
    # Translate the text to the destination language
    translated_text = translate(text, lang)

    # Synthesize the speech using the voicevox library
    asyncio.run(synthesize(translated_text, speaker=1))

    # Wait for the audio to finish playing before continuing
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)



async def synthesize(text, speaker):
    async with Client() as client:
        audio_query = await client.create_audio_query(text, speaker=speaker)
        audio_data = await audio_query.synthesis()
        with open("temp.wav", "wb") as f:
            f.write(audio_data)

    # Add a delay before attempting to open the file
    time.sleep(0.5)

    # Initialize the Pygame mixer and load the audio file
    pygame.mixer.init()
    sound = pygame.mixer.Sound("temp.wav")

    # Play the audio file and wait for it to finish playing
    # sound.play()
    # subprocess.run(['python', 'play.py'])
    Playing()
    while pygame.mixer.get_busy():
        time.sleep(1)





def translate(text, dest_lang):
    translator = Translator()
    translated_text = translator.translate(text, dest=dest_lang)
    return translated_text.text

# Set up the speech recognition engine
r = sr.Recognizer()
mic = sr.Microphone()

# Continuously listen for speech and translate/speak the input
with mic as source:
    r.adjust_for_ambient_noise(source)
    print("Listening...")
    while True:
        audio = r.listen(source)
        try:
            # Use Google's speech recognition service to convert speech to text
            text = r.recognize_google(audio, language='id')
            print("You said:", text)
            
            # Translate the text to Japanese and speak it
            translated_text = translate(text, "ja")
            print("Translation:", translated_text)
            speak(translated_text, "ja")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
