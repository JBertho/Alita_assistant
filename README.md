# Alita, l'assistant vocal qui va vous manquer

Alita n'a pas fini de vous surprendre !

## Installation

Pour lancer le projet, il vous faudra installer quelques librairies :

```bash
pip install python-dotenv
pip install simpleaudio
pip install requests
pip install pyttsx3
```

Il vous faudra ensuite créer un fichier nommé ***.env*** à la racine du projet.
Vous y mettrez les variables suivantes : 

```bash
OPEN_WEATHER_API_KEY=
JOKE_BLACKLIST_FLAGS=nsfw,racist,sexist,explicit,religious,political
```
La variable ***OPEN_WEATHER_API_KEY*** devra contenir l'api key de l'api OpenWeatherMap obtenue en vous créant un compte.

Vous pouvez ajuster la blacklist ***JOKE_BLACKLIST_FLAGS*** pour les blagues en fonction de vos sensibilités.

## Utilisation

Afin de profiter sans doute du meilleur assistant vocal de nos jours, voici ce que vous pouvez demander :

- Réveiller l'assistant en disant ***Debout Alita***
- Ecouter de la musique en disant ***Lance la musique***
- Arrêter la musique en disant ***Stop la musique***
- Rire de toutes vos larmes en disant ***Fais-moi rire !*** ou encore ***Raconte-moi une blague !***
- Mettre un rappel dans la journée en disant ***Met un rappel*** puis en lui précisant une heure dans un deuxième temps
  ainsi qu'un motif dans un troisième temps
- Regarder Alita danser en disant ***Danse !***
- Demander la météo d'une ville en disant ***Météo*** puis en lui précisant la ville dans un deuxième temps
- Mettre Alita en veille en disant ***Je te laisse***
- Laisser Alita tranquille pour de bons en lui disant ***Bonne nuit !***

Si Alita ne vous entend pas pendant plus de 30 secondes, elle s'en ira sans vous !

# Enjoy 🤖🦾🦿