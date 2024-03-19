import asyncio
import pyttsx3 
import datetime 
import speech_recognition as sr
import wikipedia
import webbrowser
# import pyaudio
import os 
import smtplib
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import cv2
import numpy as np
from tensorflow import keras
from keras.preprocessing.image import img_to_array
import pyjokes
# import threading
import keyboard
import cred
# import websockets
# import subprocess
# import http.server
# import requests

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
classifier = keras.models.load_model(r'FER_Model_Grp16.h5')

engine = pyttsx3.init('sapi5') 
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[0].id)

def say_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def open_spotify_visualization():
    # URL of the Spotify song visualization website
    url = "https://www.kaleidosync.com/spotify?access=BQAR2yIQaHEZRMvJygBUPXXPxQeX77CsJLWZ2PD5WxsjVbfGQ2YyD9G_-4Crade58an6YMz5yaUfmRGQ12JlvFBFCs6QqCN0y8Nl3OOCyxBBru0DQAFp4aDq3tW5TXROXz0N5_gtCtgPsC49ybxuNO267umMXChap4EqN15ZVAKoFMB-r6s56qQ9BxRoR_ctZ39aIbkZiiPpsAdU7vtiKAE1j-E&refresh=AQClXHt-YivaUMiCE0xvUW9m_arPMo7c5W02iKUOcg2s0nmhlhrPbUy5PR7K91Nowq1keSkV7fF5xUy_ZLdOvIRD8vFqSNeIEyymDbTRmYGH6W_lD95YGUlAn-Fssr1weFs"
    # Open the URL in the default web browser
    webbrowser.open(url)

async def play_music(song_name=None, frame=None, face_classifier=None):
    # def _play_music():
        scope = "user-library-read,user-modify-playback-state,user-read-playback-state"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            scope=scope,
            client_id="b4290497df484acea745cf0426250fcf",
            client_secret=cred.SPOTIFY_CLIENT_SECRET, 
            #os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri="http://localhost:8888/callback"
            ))
    
        # results = sp.search(q=song_name, type="track", limit=1)
    
        # if results['tracks']['items']:
        #     track_uri = results['tracks']['items'][0]['uri']
        #     sp.start_playback(uris=[track_uri])
        #     print(f"Playing {song_name}")
            
        #     while True:
        #         query = takeCommand().lower()
        #         if 'stop music' in query or 'pause music' in query:
        #             sp.pause_playback()
        #             speak('Music stopped.')
        #             break
            
        # else:
        #     print("Song not found.")
        if song_name:
            results = sp.search(q=song_name, type="track", limit=1)
            if results['tracks']['items']:
                track_uri = results['tracks']['items'][0]['uri']
                sp.start_playback(uris=[track_uri])
                print(f"Playing {song_name}")
            else:
                print("Song not found.")
        elif frame is not None and face_classifier is not None:
            dominant_emotion = get_dominant_emotion(frame, face_classifier, classifier, emotion_labels)
            mood_playlists = {
                "Neutral": "spotify:playlist:0N3B18QBwAoOqutu8T4ljt",
                "Sad": "spotify:playlist:37i9dQZF1EVJSvZp5AOML2",
            }
        
            if dominant_emotion in mood_playlists:
                playlist_uri = mood_playlists[dominant_emotion]
                sp.start_playback(context_uri=playlist_uri)
                print(f"Playing {dominant_emotion} songs from Spotify playlist.")
            else:
                print("No playlist found for the detected emotion.")

        else:
            print("Missing frame or face Classifier. Cannot determine mood.")
        
    # music_thread = threading.Thread(target=_play_music)
    # music_thread.start()
        
def stop_music():
    print("Stopping music..")
    keyboard.press_and_release('s')         
        
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# def wishMe():
#     hour = int(datetime.datetime.now().hour)
#     if hour>=0 and hour<12:
#         speak('Good Morning!')
#     elif hour>=12 and hour<18:
#         speak('Good Afternoon!')
#     else:
#         speak('Good Evening!')
#     speak('I am an Assistant. How may I help you?')
#     speak('Please say the word help manual for the command manual')
def wishMe(detected_gender):
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        if detected_gender == 'Male':
            speak('Good morning, sir!')
        else:
            speak('Good morning, mam!')
    elif hour >= 12 and hour < 18:
        if detected_gender == 'Male':
            speak('Good afternoon, sir!')
        else:
            speak('Good afternoon, mam!')
    else:
        if detected_gender == 'Male':
            speak('Good evening, sir!')
        else:
            speak('Good evening, mam!')
    speak('I am an Assistant. How may I help you?')
    speak('Please say the word help manual for the command manual')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        """ dev = sr.Microphone.list_microphone_names()
        print(dev) """
        print('Listening...')
        r.energy_threshold = 650.44
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    text_file = open("pass.txt", "r")
    data = text_file.read()
    text_file.close()
    speak('Enter password of your email')
    pwd = input("Enter Password: ")
    if pwd == data:
        server.login('yuvrajsigh1402@gmail.com', data)
    server.sendmail('yuvrajsigh1402@gmail.com', to, content)
    server.close()
    
def get_dominant_emotion(frame, face_classifier, classifier, emotion_labels):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) > 0:

        (x, y, w, h) = faces[0]
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
        
        roi = roi_gray.astype('float') / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)

        predictions = classifier.predict(roi)[0]
        emotion_label = emotion_labels[np.argmax(predictions)]
        return emotion_label
    else:
        return 'Neutral'

async def display_help():
    commands = {
        'wikipedia': 'Search for information on Wikipedia.',
        'open youtube': 'Open YouTube in the default web browser.',
        'open google': 'Open Google in the default web browser.',
        'the time': 'Get the current time.',
        'play music': 'Play music from Spotify.',
        'open code': 'Open Visual Studio Code.',
        'change voice': 'Change the voice of the assistant.',
        'email to yuvraj': 'Send an email to a specific email address.',
        'stop Assistant': 'Stop the assistant and exit the program.',
        'open face recognition': 'Open the F-E-R System (Face Expression Recognition System).',
        'stop emotion detection': 'Stop detecting emotions from the webcam feed.',
        'detect emotion': 'Detect the emotion from the webcam feed.',
    }
    
    for command, description in commands.items():
        print(f"{command}: {description}")

# if __name__ == '__main__':
async def main():
    face_classifier = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
    emotion_detection_enabled = True
    cap = cv2.VideoCapture(0)
    
    from detect import get_gender

    _, frame = cap.read()

# Detect the user's gender
    detected_gender = get_gender(frame)

# Call the updated wishMe function with the detected gender
    # wishMe(detected_gender)
    # wishMe()
    
    if detected_gender == 'Male':
        engine.setProperty('voice', voice[0].id)  # Set male voice
    elif detected_gender == 'Female':
        engine.setProperty('voice', voice[1].id)  # Set female voice
    else:
        print("Unable to detect gender. Using default voice.")
        detected_gender = None

    # Greet the user based on the detected gender
    wishMe(detected_gender)
    
    while True: #if 1 for listening one time
        query = takeCommand().lower()
        if 'wikipedia' in query:
            try:
                speak('Searching Wikipedia...')
                query = query.replace('wikipedia', '')
                results = wikipedia.summary(query, sentences=2)
                speak('According to Wikipedia')
                speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("There are multiple options for this query. Please choose from the following:")
                options = e.options[:5]  # Display the first 5 options
                for i, option in enumerate(options, start=1):
                    speak(f"{i}. {option}")
                
                choice = None
                while choice is None:
                    choice_text = takeCommand()
                    try:
                        choice = int(choice_text)
                    except ValueError:
                        speak("Please say the number of the option you want to learn more about.")
                
                try:
                    results = wikipedia.summary(options[choice - 1], sentences=2)
                    speak('According to Wikipedia')
                    speak(results)
                except (IndexError, ValueError):
                    speak("Invalid choice. Please try again.")

        elif 'open youtube' in query:
            webbrowser.open('youtube.com')
        
        elif 'help manual' in query:
            await display_help()
        
        elif 'open google' in query:
            webbrowser.open('google.com')

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime('%H:%M:%S')
            speak(f'The time is {strTime}')
        
        elif 'play music' in query:
            speak("What song would you like to play?")
            song_name = takeCommand().lower()
            await play_music(song_name)
            spotify_visual = True
            open_spotify_visualization()
            
        elif 'open code' in query:
            codePath = "C:\\Users\\Yuvraj Singh\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
        
        elif 'change voice' in query:
            engine.setProperty('voice', voice[1].id)
            speak('Hi!')
            
        elif 'stop Assistant' in query or 'exit' in query:
            speak("Goodbye! Have a great day.")
            break
        
        elif 'email to yuvraj' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "ym3240@srmist@edu.in"
                sendEmail(to, content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak("Email not sent")
                
                
        elif 'open face recognition' in query:
            speak("Opening The F-E-R System")
            try:
                os.system('python main.py')
            except Exception as e:
                print(f"Error running face Expression recognition: {e}")
                
        elif 'stop emotion detection' in query or 'exit emotion detection' in query:
            speak("Stopping emotion detection")
            emotion_detection_enabled = False
            cap.release()
            cv2.destroyAllWindows()
                
        elif ('detect emotion' in query) and emotion_detection_enabled:
            cap.release()
            cap = cv2.VideoCapture(0)
            _, frame = cap.read()

            if not frame is None:
                dominant_emotion = get_dominant_emotion(frame, face_classifier, classifier, emotion_labels)
                speak(f"You seem to be {dominant_emotion.lower()} right now.")
                
                if dominant_emotion.lower() == 'sad':
                    speak("Would you like to hear a joke or a song to cheer up?")
                    user_preference = takeCommand().lower()
                    if 'joke' in user_preference:
                        speak("Here is a joke to cheer you up")
                        say_joke()
                    elif 'song' in user_preference:
                        await play_music(frame=frame, face_classifier=face_classifier)
                        open_spotify_visualization()
                    else:
                        speak("I'm sorry, I didn't understand your preference.")
                
                elif dominant_emotion.lower() == 'neutral':
                    speak("Being productive is key to staying happy. Would you like music to focus?")
                    user_preference = takeCommand().lower()
                    if 'yes' in user_preference:
                        await play_music(frame=frame, face_classifier=face_classifier)
                    else:
                        speak("Okay, Let me know if you need anyhting else.")
            
            else:
                speak("Error detecting emotion. Please try again")
                
        elif 'start emotion detection' in query:
            speak("Starting emotion detection")
            emotion_detection_enabled = True
            cap.release()  
            cap = cv2.VideoCapture(0)
            _, frame = cap.read()

            if not frame is None:
                dominant_emotion = get_dominant_emotion(frame, face_classifier, classifier, emotion_labels)
                speak(f"You seem to be {dominant_emotion.lower()} right now.")
                
            else:
                speak("Error detecting emotion. Please try again.")
                
if __name__ == '__main__':
    asyncio.run(main())
    # start_visualizer_server()