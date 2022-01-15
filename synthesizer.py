import pyttsx3


class Synthesizer:
    def __init__(self):
        self.synthesizer = pyttsx3.init()
        voices = self.synthesizer.getProperty("voices")
        self.synthesizer.setProperty('voice', voices[3].id)

    def talk(self, output):
        self.synthesizer.say(output)
        self.synthesizer.runAndWait()
        self.synthesizer.stop()