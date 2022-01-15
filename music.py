import simpleaudio as sa


class Music:
    currentSongPlaying = None

    @staticmethod
    def play_song():
        try:
            Music.stop_song()
            songToPlay = sa.WaveObject.from_wave_file("music/alita_song.wav")
            Music.currentSongPlaying = songToPlay.play()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def stop_song():
        if Music.currentSongPlaying is not None:
            Music.currentSongPlaying.stop()
            return True
        return False
