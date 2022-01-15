from datetime import datetime


class Reminder:

    def __init__(self, hour: datetime, reason: str):
        self.__hour = hour
        self.__reason = reason

    @property
    def hour(self):
        return self.__hour

    @property
    def reason(self):
        return self.__reason
