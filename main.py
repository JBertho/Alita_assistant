# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
from datetime import datetime
import pyaudio
import speech_recognition as sr
import time
import requests
from dotenv import load_dotenv

from Reminder import Reminder
from music import Music
import pyttsx3

from synthesizer import Synthesizer

recognizer = sr.Recognizer()
reminders = list()


def start_recognition(recognizer):
    with sr.Microphone() as source:
        if Music.is_playing():
            recognizer.energy_threshold = 2000
        else:
            recognizer.energy_threshold = 300

        print("J'écoute")
        audio = recognizer.listen(source,timeout=8,phrase_time_limit=3)
        print("J'ai entendu")
        try:
            statement = recognizer.recognize_google(audio, language='fr-FR')
            if statement is None:
                print("Je passe la")
                return ""
            else:
                return statement.lower()
        except Exception as e:
            print(e)
            return ""


def containWakeUpWord(statement):
    return "debout alita" in statement or "debout anita" in statement or "debout aliba" in statement or "debout anita" in statement


def containSleepWord(statement):
    return "je te laisse" in statement


def start_dancing():
    for i in range(10):
        print("♪┏( ・o･)┛♪┗ ( ･o･) ┓♪\n")
        time.sleep(1)
        print("♪┗ (・o･ )┓♪┏ (･o･ ) ┛♪\n")
        time.sleep(1)


def findActionToDo(statement, synthesizer):
    global last_action_time
    global is_listening
    if "danse" in statement:
            start_dancing()
    elif "lance la musique" in statement:
        result = Music.play_song()
        if result:
            synthesizer.talk("C'est partie !")
        else:
            synthesizer.talk("Je n'ai pas pu lancer le son")
    elif "stop" in statement and "musique" in statement:
        result = Music.stop_song()
        if result:
            synthesizer.talk("J'ai arreté la musique")
        else:
            synthesizer.talk("Il n'y avait rien a arreté")
    elif "météo" in statement or "temps" in statement:
        synthesizer.talk(get_city_weather(statement.split()[-1]))
    elif "blague" in statement or "rire" in statement:
        get_joke(synthesizer)
    elif "rappel" in statement:
        synthesizer.talk("Pour quelle heure ?")
        hour = start_recognition(recognizer=recognizer)
        synthesizer.talk("OK ! Quel est le motif de ce rappel ?")
        reason = start_recognition(recognizer=recognizer)
        add_reminder(hour, reason)
    else:
        current_time = datetime.now()
        if is_listening and (current_time - last_action_time).total_seconds() > 60:
            is_listening = False
            synthesizer.talk("Je me rendors")
        elif len(statement) > 0:
            synthesizer.talk("Je n'ai pas compris ton message")
    last_action_time = datetime.now()

def contain_weather_word(statement):
    return "meteo" in statement


def get_city_weather(city: str):
    try:
        open_weather_api_key = os.getenv("OPEN_WEATHER_API_KEY")
        data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&lang=fr&units=metric&APPID={open_weather_api_key}"
        ).json()
        temperature_in_degree = data.get('main')['temp']
        weather_description = data.get('weather')[0].get('description')

        return f"A {city}, il fait {temperature_in_degree}°C avec un temps {weather_description}"

    except:
        return "Désolé, mais je ne connais pas cette ville sur la planète Terre 🤖"


def get_joke(synthesizer):
    try:
        blacklist_flags = os.getenv('JOKE_BLACKLIST_FLAGS')
        data = requests.get(
            f" https://v2.jokeapi.dev/joke/Any?lang=fr&blacklistFlags={blacklist_flags}"
        ).json()

        if data.get('type') == "single":
            synthesizer.talk(data.get('joke'))
        else:
            synthesizer.talk(data.get('setup'))
            time.sleep(1)
            synthesizer.talk(data.get('delivery'))
    except:
        synthesizer.talk("Oups, celle-ci était un peu trop violente pour vous 🤖")


last_action_time = datetime.now()
is_listening = False


def add_reminder(hour: str, reason: str):
    try:
        date_time_obj = datetime.strptime(hour, '%Hh%M')
        reminder = Reminder(date_time_obj, reason)
        reminders.append(reminder)
        print(f"OK ! Rappel programmé à {reminder.hour} pour {reminder.reason}")
    except:
        print("Oops, le rappel n'a pas pu être programmé !")


def check_reminders():
    now = datetime.now()
    for index, reminder in enumerate(reminders):
        if reminder.hour.time() <= now.time():
            print(f"RAPPEL : {reminder.reason}")
            reminders.pop(index)


def start_alita(synthesizer):
    recognizer = sr.Recognizer()
    print("Lancement d'Alita")
    isAwake = True
    global is_listening
    global last_action_time
    while isAwake:
        check_reminders()
        statement = start_recognition(recognizer=recognizer)
        print("test valeur = " + statement)
        if containWakeUpWord(statement):
            synthesizer.talk("Salut mec")
            is_listening = True
        elif containSleepWord(statement):
            is_listening = False
            synthesizer.talk("A la prochaine")
        elif is_listening:
            findActionToDo(statement,synthesizer)

        elif "bonne nuit" in statement:
            isAwake = False
            synthesizer.talk("Au revoir")
        else:
            synthesizer.talk("Je n'ai pas compris")


if __name__ == '__main__':
    load_dotenv()
    synthesizer = Synthesizer()
    start_alita(synthesizer)
    #synthesizer.talk("Bonjour alban le grand maitre")
