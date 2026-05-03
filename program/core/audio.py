import pygame


class AudioSystem:
    def __init__(self) -> None:
        self.ready = False
        self.sounds = {}

    def init(self) -> None:
        try:
            pygame.mixer.init()
            self.ready = True
        except pygame.error:
            self.ready = False

    def play(self, key: str) -> None:
        if not self.ready:
            return
        snd = self.sounds.get(key)
        if snd:
            snd.play()
