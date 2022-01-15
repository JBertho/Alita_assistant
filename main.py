import speech_recognition as sr
import time

from music import Music

global currentSongPlaying


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
    for i in range(10) :
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
    else:
        print("Je n'ai pas compris ton message")

def start_alita():
    recognizer = sr.Recognizer()
    print("Lancement d'Alita")
    isAwake = True
    isListening = False
    while isAwake:
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
    start_alita()
