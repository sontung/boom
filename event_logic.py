import pygame
import sys
import time
from pygame.locals import *


class TimeTracking:
    def __init__(self, number_of_seconds, sprite):
        self.number_of_seconds = number_of_seconds
        self.time_at_the_moment = time.time()
        self.sprite = sprite

    def time_up(self):
        """
        Check to see if the amount of self.number_of_seconds seconds has passed
        """
        if time.time() - self.time_at_the_moment >= self.number_of_seconds:
            return True
        else:
            return False

    def set_time(self, val):
        self.time_at_the_moment = time.time()
        self.number_of_seconds = val

    def get_sprite(self):
        return self.sprite

    def trigger(self, func):
        """
        Run the func function and time is up
        """
        if self.time_up():
            func()
            return True
        return False


class EventLogic:
    def __init__(self, _game_state, _game_gui, _sound):
        self._game_state = _game_state
        self._game_gui = _game_gui
        self._sound = _sound
        self.number_of_handler_executions = 0
        self.movement = {
            K_UP: "up",
            K_DOWN: "down",
            K_RIGHT: "right",
            K_LEFT: "left"
        }
        self.time_trackers = []

    def quit(self):
        pygame.quit()
        sys.exit()

    def event_handler(self):
        for time_tracker in self.time_trackers:
            if time_tracker.trigger(time_tracker.get_sprite().explode):
                self._sound.set_state(2)
                self._sound.play_sound()
                self._sound.force_play()
                self._game_state.track_players_bombs(time_tracker.get_sprite())
                self._game_state.track_treasures(time_tracker.get_sprite())
                time_tracker.set_time(0.3)
                self._game_gui.add_time_tracker(time_tracker)
                self.time_trackers.remove(time_tracker)
                self._game_gui.map.remove_sprite(time_tracker.get_sprite())

        event = pygame.event.poll()
        if event.type == MOUSEBUTTONUP:
            if self._game_state.get_state() == "welcome":
                if self._game_gui.new.get_rect().collidepoint(event.pos):
                    self._game_gui.reset()
                    self._game_state.reset()
                    self._game_state.set_state("new game")
                    self._sound.stop_sound()
                elif self._game_gui.help.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("help")
                elif self._game_gui.author.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("author")
                elif self._game_gui.quit.get_rect().collidepoint(event.pos):
                    self.quit()
            elif self._game_state.get_state() in ["help", "author"]:
                if self._game_gui.back.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("welcome")
            elif self._game_state.get_state() == "game over":
                if self._game_gui.back.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("welcome")
                    self._sound.stop_sound()
                elif self._game_gui.play_again.get_rect().collidepoint(event.pos):
                    self._game_gui.reset()
                    self._game_state.reset()
                    self._game_state.set_state("new game")
                    self._sound.stop_sound()

        elif event.type == MOUSEMOTION or event.type == NOEVENT:
            if self._game_gui.buttons:
                self._game_gui.draw(self._game_state.get_state())
                for button in self._game_gui.buttons:
                    button.set_bold(pygame.mouse.get_pos())
                pygame.display.update()

        elif event.type == pygame.QUIT:
            self.quit()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.quit()

            elif event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                if self._game_state.get_state() == "new game":
                    while pygame.key.get_pressed()[event.key]:
                        for sprite in self._game_gui.get_characters():
                            sprite.increment_pos(self.movement[event.key])
                            self._game_gui.draw("new game")
                            pygame.display.update()
                            pygame.time.wait(20)
                            sprite.increment_pos(self.movement[event.key])
                            self._game_gui.draw("new game")
                            pygame.display.update()
                            pygame.time.wait(20)
                            sprite.increment_pos(self.movement[event.key])
                            self._game_gui.draw("new game")
                            pygame.display.update()
                        pygame.time.wait(100)
                        self.event_handler()

            elif event.key == K_SPACE:
                if self._game_state.get_state() == "new game":
                    char_pos = self._game_gui.characters[0].get_pos()[0]-4, self._game_gui.characters[0].get_pos()[1]
                    boom = self._game_gui.create_boom(char_pos)
                    self._game_gui.map.add_sprites(boom, "bomb")
                    boom_trigger = TimeTracking(2, boom)
                    self.time_trackers.append(boom_trigger)
                    pygame.display.update()

            elif event.key == K_e:
                if self._game_state.get_state() == "new game":
                    self._game_gui.set_request_open_door()