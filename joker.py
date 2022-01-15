import requests
import os

from joke import Joke


class Joker:

    def get_joke(self) -> Joke:
        try:
            blacklist_flags = os.getenv('JOKE_BLACKLIST_FLAGS')
            data = requests.get(
                f" https://v2.jokeapi.dev/joke/Any?lang=fr&blacklistFlags={blacklist_flags}"
            ).json()
            return Joke(data.get('type'), data.get('joke'), data.get('setup'), data.get('delivery'))
        except:
            return Joke("single", "Oups, celle-ci était un peu trop violente pour vous 🤖")
