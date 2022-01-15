class Joke:

    def __init__(self, joke_type: str, joke: str = "", setup: str = "", delivery: str = ""):
        self.__joke_type = joke_type
        self.__joke = joke
        self.__setup = setup
        self.__delivery = delivery

    @property
    def joke(self) -> str:
        return self.__joke

    @property
    def joke_type(self) -> str:
        return self.__joke_type

    @property
    def setup(self) -> str:
        return self.__setup

    @property
    def delivery(self) -> str:
        return self.__delivery
