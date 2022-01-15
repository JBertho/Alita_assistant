import simpleaudio as sa


class Music:
    current_song_playing = None

    @staticmethod
    def play_song():
        try:
            Music.stop_song()
            song_to_play = sa.WaveObject.from_wave_file("music/alita_song.wav")
            Music.current_song_playing = song_to_play.play()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def stop_song():
        if Music.current_song_playing is not None:
            Music.current_song_playing.stop()
            Music.current_song_playing = None
            return True
        return False

    @staticmethod
    def is_playing() -> bool:
        return Music.current_song_playing is not None and Music.current_song_playing.is_playing()
