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

global currentSongPlaying

recognizer = sr.Recognizer()
reminders = list()


def start_recognition(recognizer):
    with sr.Microphone() as source:
        if Music.is_playing():
            recognizer.energy_threshold = 2000
        else:
            recognizer.energy_threshold = 300

        print("J'écoute")
        audio = recognizer.listen(source)
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
    return "debout alita" in statement or "debout anita" in statement or "debout aliba" in statement


def containSleepWord(statement):
    return "je te laisse" in statement


def start_dancing():
    for i in range(10):
        print("♪┏( ・o･)┛♪┗ ( ･o･) ┓♪\n")
        time.sleep(1)
        print("♪┗ (・o･ )┓♪┏ (･o･ ) ┛♪\n")
        time.sleep(1)


def findActionToDo(statement):
    if "danse" in statement:
        for i in range(10):
            start_dancing()
    elif "lance la musique" in statement:
        result = Music.play_song()
        if result:
            print("C'est partie !")
        else:
            print("Je n'ai pas pu lancer le song")
    elif "stop" in statement and "musique" in statement:
        result = Music.stop_song()
        if result:
            print("J'ai arreté la musique")
        else:
            print("Il n'y avait rien a arreté")
    elif "météo" in statement or "temps" in statement:
        get_city_weather(statement.split()[-1])
    elif "blague" in statement or "rire" in statement:
        get_joke()
    elif "rappel" in statement:
        print("Pour quelle heure ?")
        hour = start_recognition(recognizer=recognizer)
        print("OK ! Quel est le motif de ce rappel ?")
        reason = start_recognition(recognizer=recognizer)
        add_reminder(hour, reason)
    else:
        print("Je n'ai pas compris ton message")


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
        print(
            f"A {city}, il fait {temperature_in_degree}°C avec un temps {weather_description}"
        )
    except:
        print("Désolé, mais je ne connais pas cette ville sur la planète Terre 🤖")


def get_joke():
    try:
        blacklist_flags = os.getenv('JOKE_BLACKLIST_FLAGS')
        data = requests.get(
            f" https://v2.jokeapi.dev/joke/Any?lang=fr&blacklistFlags={blacklist_flags}"
        ).json()

        if data.get('type') == "single":
            print(data.get('joke'))
        else:
            print(data.get('setup'))
            print(data.get('delivery'))
    except:
        print("Oups, celle-ci était un peu trop violente pour vous 🤖")


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


def start_alita():
    print("Lancement d'Alita")
    isAwake = True
    isListening = False
    while isAwake:
        check_reminders()
        statement = start_recognition(recognizer=recognizer)
        print("test valeur = " + statement)
        if containWakeUpWord(statement):
            print("Salut mec")
            isListening = True
        elif containSleepWord(statement):
            isListening = False
            print("A la prochaine")
        elif isListening:
            findActionToDo(statement)

        elif "bonne nuit" in statement:
            isAwake = False
            print("Au revoir")
        else:
            print("Je n'ai pas compris")


if __name__ == '__main__':
    load_dotenv()
    start_alita()
