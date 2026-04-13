import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from datetime import datetime

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print("Jarvis:", text)   
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    print("Command received:", c) 

    if "open google" in c.lower():    # Open Google
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open youtube" in c.lower():   # Open YT
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c.lower(): # Open LinkedIn
        speak("Opening Linkedin")
        webbrowser.open("https://www.linkedin.com/feed/")

    elif "open instagram" in c.lower():  # Open Insta
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com")

    elif c.lower().startswith("play"): # Play song on Spotify
        if ("spotify") in c.lower():
            song = c.lower().replace("play", "").strip()
            song = song.lower().replace("on spotify", "").strip()
            webbrowser.open(f"https://open.spotify.com/search/{song}")
        
        else:
            song = c.lower().replace("play", "").strip()
            webbrowser.open(f"https://open.spotify.com/search/{song}")

    elif c.lower().startswith("search"): # Search on YT
        if("youtube") in c.lower():
            video = c.lower().replace("search", "").strip()
            video = video.lower().replace("on youtube", "").strip()
            webbrowser.open(f"https://www.youtube.com/results?search_query={video}")

        else:
            video = c.lower().replace("search", "").strip()
            webbrowser.open(f"https://www.youtube.com/results?search_query={video}")

    elif "tell me score" in c.lower(): # Cricket match score

        speak("Fetching latest score")

        url = "https://api.cricapi.com/v1/currentMatches?apikey=5ab0ce63-45b0-4a13-9d7a-472445d3864e"
    
        try:
            response = requests.get(url)
            data = response.json()

            # Take first match
            match = data["data"][0]

            team1 = match["teamInfo"][0]["shortname"]
            team2 = match["teamInfo"][1]["shortname"]

            score1 = match["score"][0]
            runs = score1["r"]
            wickets = score1["w"]

            status = match["status"]

            result = f"{team1} scored {runs} for {wickets}. {status}"

            print(result)
            speak(result)

        except Exception as e:
            print("Error:", e)
            speak("Sorry, I could not fetch the score")

    elif "tell me time" in c.lower():  # Time
        current_time = datetime.now().strftime("%H:%M")
        speak(f"The time is {current_time}")

    elif "tell me weather" in c.lower(): # Weather

        speak("Fetching weather")

        url = "https://api.openweathermap.org/data/2.5/weather?q=Jaipur&appid=4a1939b340bb6e17bc6cefb9797335a2&units=metric"

        response = requests.get(url)
        data = response.json()

        temp = data["main"]["temp"]
        condition = data["weather"][0]["description"]

        result = f"The temperature is {temp} degrees and weather is {condition}"

        print(result)
        speak(result)

    elif "who are you" in c.lower():  # Introduction
        speak("I am Jarvis, your personal voice assistant. I can help you with tasks like playing music, telling time, and more.")

    elif "who created you" in c.lower():  # Creator Intro
        speak("I was created by Harshvardhan Singh, a B.Tech Computer Science student in AI and ML at JECRC University, as part of his learning and development in AI projects.")



if __name__ == "__main__":
    speak("Initializing Jarvis.....")

    while True:
        recognizer = sr.Recognizer()

        print("Recognizing...")   

        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)

            word = recognizer.recognize_google(audio)
            print("You said :", word)  

            if(word.lower() == "jarvis"):
                speak("Yes")

                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source)
                    print("Jarvis Active... Listening for command...")
                    audio = recognizer.listen(source)

                    command = recognizer.recognize_google(audio)
                    print("You said (command):", command)   

                    processCommand(command)

        except Exception as e:
            print("Error:", e)