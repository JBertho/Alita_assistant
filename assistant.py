from datetime import datetime

import speech_recognition as sr

from joker import Joker
from reminder import Reminder
from synthesizer import Synthesizer
from music import Music
import time

from weather import Weather


class Assistant:

    def __init__(self):
        self.__recognizer = sr.Recognizer()
        self.__synthesizer = Synthesizer()
        self.__awake = True
        self.__listening = False
        self.__last_action_time = datetime.now()
        self.__reminders: [Reminder] = []
        self.__joker = Joker()
        self.__weather = Weather()

    @property
    def recognizer(self):
        return self.__recognizer

    @property
    def synthesizer(self):
        return self.__synthesizer

    @property
    def last_action_time(self) -> datetime:
        return self.__last_action_time

    @last_action_time.setter
    def last_action_time(self, value):
        self.__last_action_time = value

    @property
    def listening(self) -> bool:
        return self.__listening

    @listening.setter
    def listening(self, value: bool):
        self.__listening = value

    @property
    def awake(self) -> bool:
        return self.__awake

    @awake.setter
    def awake(self, value: bool):
        self.__awake = value

    def talk(self, speech: str):
        self.__synthesizer.talk(speech)

    def listen(self) -> str:
        with sr.Microphone() as source:
            if Music.is_playing():
                self.__recognizer.energy_threshold = 2000
            else:
                self.__recognizer.energy_threshold = 300

            print("J'écoute")
            audio = self.__recognizer.listen(source, timeout=8, phrase_time_limit=3)
            print("J'ai entendu")
            try:
                statement = self.__recognizer.recognize_google(audio, language='fr-FR')
                if statement is None:
                    print("Je passe la")
                    return ""
                else:
                    return statement.lower()
            except Exception as e:
                print(e)
                return ""

    def tell_joke(self):
        joke = self.__joker.get_joke()

        if joke.joke_type == "single":
            self.talk(joke.joke)
        else:
            self.talk(joke.setup)
            time.sleep(2)
            self.talk(joke.delivery)

    def tell_weather(self, city: str):
        city_weather = self.__weather.get_city_weather(city)
        self.talk(city_weather)

    def ask_reminder_hour(self) -> str:
        self.talk("Pour quelle heure ?")
        hour = self.listen()
        return hour

    def ask_reminder_reason(self) -> str:
        self.talk("OK ! Quel est le motif de ce rappel ?")
        reason = self.listen()
        return reason

    def add_reminder(self):
        hour = self.ask_reminder_hour()
        self.talk("OK ! Quel est le motif de ce rappel ?")
        reason = self.ask_reminder_reason()
        try:
            date_time_obj = datetime.strptime(hour, '%Hh%M')
            reminder = Reminder(date_time_obj, reason)
            self.__reminders.append(reminder)
            self.talk(f"OK ! Rappel programmé à {reminder.hour} pour {reminder.reason}")
        except:
            self.talk("Oops, le rappel n'a pas pu être programmé !")

    def check_reminders(self):
        now = datetime.now()
        for index, reminder in enumerate(self.__reminders):
            if reminder.hour.time() <= now.time():
                self.talk(f"RAPPEL : {reminder.reason}")
                self.__reminders.pop(index)
