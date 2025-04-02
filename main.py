import os
import eel
from backend.auth import recoganize
from backend.auth.recoganize import AuthenticateFace
from backend.feature import *
from backend.command import *



def send_message_to_frontend(message):
    print(f"Sending message: {message}")  # Debugging line
    eel.updateFrontend(message)  # This line sends the message to the frontend

def start():
    
    eel.init("frontend") 
    
    play_assistant_sound()
    @eel.expose
    def init():
        eel.hideLoader()
        speak("Welcome to Jarvis")
        speak("Ready for Face Authentication")
        flag = recoganize.AuthenticateFace()
        if flag ==1:
            speak("Face recognized successfully")
            eel.hideFaceAuth()
            eel.hideFaceAuthSuccess()
            speak("Welcome to Your Assistant")
            eel.hideStart()
            play_assistant_sound()
        else:
            speak("Face not recognized. Please try again")
        
    os.system('start chrome --app="http://127.0.0.1:8000/index.html"')  # Change to Google Chrome
    
    
    
    eel.start("index.html", mode=None, host="localhost", block=True) 

