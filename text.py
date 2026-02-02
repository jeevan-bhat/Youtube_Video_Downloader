import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import requests
import openai

WEATHER_API_KEY = "YOUR_APY_KEY"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
openai.api_key=OPENAI_API_KEY
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_user():
    now = datetime.datetime.now().hour
    # print(now)
    if now <12:
        speak("Good Morning lord")
    elif 12< now <18:
        speak("Good Afternoon lord")
    else:
        speak("Good Night lord")


def take_command():
    sp=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        sp.pause_threshold = 1
        audio=sp.listen(source)

    try:
        command=sp.recognize_bing(audio)
        print("you said :",command)
        return command.lower()
    except:
        speak("Sorry, I didn't catch that")
        return ""

def weather(city):
    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response=requests.get(url).json()

    if response["cod"] !=200:
        speak("city not found")

    else:
        temp=response["main"]["temp"]
        desc=response["weather"][0]["description"]
        speak(f"The temperature in {city} is {temp} degrees Celsius with {desc}")

def open_ai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message.content
        speak(reply)

    except:
        speak("cant connect to open ai")





greet_user()

speak("iam your voice assistant How can I help you")


while True:
    command=take_command()

    if "time"==command:
        time=datetime.datetime.now().strftime("%H:%M")
        speak(f"the time is {time}")

    elif "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")

    elif "weather" in command:
        speak("tell me the city name")
        city=take_command()
        weather(city)

    elif "ask" in command:
        speak("what do you want to ask")
        question=take_command()
        open_ai(question)

    elif "exit" or "quit" in command:
        speak("goodye shuttting down")
        break
