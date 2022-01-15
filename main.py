# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from datetime import datetime
import time
from dotenv import load_dotenv

from assistant import Assistant
from music import Music


def contain_wake_up_word(statement: str) -> bool:
    return "debout alita" in statement or "debout anita" in statement or "debout aliba" in statement or "debout anita" in statement


def contain_sleep_word(statement: str) -> bool:
    return "je te laisse" in statement


def contain_weather_word(statement: str) -> bool:
    return "météo" in statement or "temps" in statement


def contain_dance_word(statement: str) -> bool:
    return "danse" in statement


def contain_launch_music_word(statement: str) -> bool:
    return "lance la musique" in statement


def contain_stop_music_word(statement: str) -> bool:
    return "stop" in statement and "musique" in statement


def contain_joke_word(statement: str) -> bool:
    return "blague" in statement or "rire" in statement


def contain_reminder_word(statement: str) -> bool:
    return "rappel" in statement


def start_dancing():
    for i in range(10):
        print("♪┏( ・o･)┛♪┗ ( ･o･) ┓♪\n")
        time.sleep(1)
        print("♪┗ (・o･ )┓♪┏ (･o･ ) ┛♪\n")
        time.sleep(1)


def find_action_to_do(statement: str, alita: Assistant):
    if contain_dance_word(statement):
        start_dancing()
    elif contain_launch_music_word(statement):
        result = Music.play_song()
        if result:
            alita.talk("C'est partie !")
        else:
            alita.talk("Je n'ai pas pu lancer le son")
    elif contain_stop_music_word(statement):
        result = Music.stop_song()
        if result:
            alita.talk("J'ai arreté la musique")
        else:
            alita.talk("Il n'y avait rien a arreté")
    elif contain_weather_word(statement):
        alita.tell_weather(statement.split()[-1])
    elif contain_joke_word(statement):
        alita.tell_joke()
    elif contain_reminder_word(statement):
        alita.add_reminder()
    else:
        current_time = datetime.now()
        if alita.listening and (current_time - alita.last_action_time).total_seconds() > 60:
            alita.listening = False
            alita.talk("Je me rendors")
        elif len(statement) > 0:
            alita.talk("Je n'ai pas compris ton message")
    alita.last_action_time = datetime.now()


def start_alita():
    print("Lancement d'Alita")
    alita = Assistant()

    while alita.awake:
        alita.check_reminders()
        statement = alita.listen()
        print("test valeur = " + statement)

        if contain_wake_up_word(statement):
            alita.talk("Salut mec")
            alita.awake = True
        elif contain_sleep_word(statement):
            alita.listening = False
            alita.talk("A la prochaine")
        elif alita.listening:
            find_action_to_do(statement, alita)
        elif "bonne nuit" in statement:
            alita.awake = False
            alita.talk("Au revoir")
        else:
            alita.talk("Je n'ai pas compris")


if __name__ == '__main__':
    load_dotenv()
    start_alita()
