import time
import pyttsx3
import speech_recognition as sr
import eel

def send_message_to_frontend(message):
    print(f"Message before sending: {message}")  # Log the entire message structure
    if 'value' not in message:
        message['value'] = "Default message"  # Ensure 'value' key exists
    print(f"Sending message: {message}")  # Debugging line
    print(f"Message before sending: {message}")  # Log the entire message structure
    if 'value' not in message:
        message['value'] = "Default message"  # Ensure 'value' key exists
    print(f"Sending message: {message}")  # Debugging line
    if 'value' not in message:
        message['value'] = "Default message"  # Ensure 'value' key exists
    print(f"Sending message: {message}")  # Debugging line
    print(f"Sending message: {message}")  # Debugging line
    eel.updateFrontend(message)  # This line sends the message to the frontend

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    # print(voices)
    engine.setProperty('voice', voices[2].id)
    print(f"Sending message to frontend: {{'value': {text}}}")
    eel.DisplayMessage({'value': text})
    engine.say(text)
    engine.runAndWait()
    engine.setProperty('rate', 174)
    eel.receiverText(text)

# Expose the Python function to JavaScript

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I'm listening...")
        eel.DisplayMessage("I'm listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 8)

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
        eel.DisplayMessage({'value': query})
        
        
        speak(query)
    except Exception as e:
        print(f"Error: {str(e)}\n")
        return None

    return query.lower()



@eel.expose
def takeAllCommands(message=None):
    if message is None:
        query = takecommand()  # If no message is passed, listen for voice input
        if not query:
            return  # Exit if no query is received
        print(query)
        eel.senderText(query)
    else:
        query = message  # If there's a message, use it
        print(f"Message received: {query}")
        eel.senderText(query)
    
    try:
        if query:
            if "open" in query:
                from backend.feature import openCommand
                openCommand(query)
            elif "send message" in query or "call" in query or "video call" in query:
                from backend.feature import findContact, whatsApp
                flag = ""
                Phone, name = findContact(query)
                if Phone != 0:
                    if "send message" in query:
                        flag = 'message'
                        speak("What message to send?")
                        query = takecommand()  # Ask for the message text
                    elif "call" in query:
                        flag = 'call'
                    else:
                        flag = 'video call'
                    whatsApp(Phone, query, flag, name)
            elif "on youtube" in query:
                from backend.feature import PlayYoutube
                PlayYoutube(query)
            else:
                from backend.feature import chatBot
                chatBot(query)
        else:
            speak("No command was given.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Something is wrong.")
    
    eel.ShowHood()
