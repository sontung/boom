import pygame


class Sound:
    def __init__(self):
        self.state_of_sound = None
        self.ready_to_play = True
        self.file_names = {
            0: "assets\sounds\\background.mid",  # background music
            1: pygame.mixer.Sound("assets\sounds\\beep.ogg"),  # click sound
            2: pygame.mixer.Sound("assets\sounds\\explosion.wav"),  # explosion effect
            3: "assets\sounds\\ending.mp3",  # ending music
            4: pygame.mixer.Sound("assets\sounds\\item.mp3"),  # item buff
            5: pygame.mixer.Sound("assets\sounds\\monsterkilled.mp3"),  # monster killed
            6: pygame.mixer.Sound("assets\sounds\\door_open.ogg"),  # door opening
            7: pygame.mixer.Sound("assets\sounds\\death.wav"),  # player lost 1 live
            8: pygame.mixer.Sound("assets\sounds\\round_end.wav")  # player lost all lives
        }

    def set_state(self, val):
        self.state_of_sound = val

    def play_sound(self):
        if self.state_of_sound is not None and self.ready_to_play:
            self.ready_to_play = False
            if self.state_of_sound in [0, 3]:
                pygame.mixer.music.load(self.file_names[self.state_of_sound])
                pygame.mixer.music.play(-1)
            else:
                self.file_names[self.state_of_sound].play()

    def force_play(self):
        self.ready_to_play = True

    def stop_sound(self):
        if self.state_of_sound == 0:
            pygame.mixer.music.stop()
        else:
            self.file_names[self.state_of_sound].stop()
        self.ready_to_play = True
        self.set_state(None)
