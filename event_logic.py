import pygame
import sys
import time
from pygame.locals import *


class TimeTracking:
    def __init__(self, number_of_seconds, boom, _game_state):
        self.number_of_seconds = number_of_seconds
        self.time_at_the_moment = time.time()
        self.boom = boom
        self.state = _game_state

    def time_up(self):
        """
        Check to see if the amount of self.number_of_seconds seconds has passed
        """
        if time.time() - self.time_at_the_moment >= self.number_of_seconds:
            return True
        else:
            return False

    def get_boom(self):
        return self.boom

    def trigger(self):
        """
        Explode the bomb after time is up
        """
        if self.time_up():
            self.boom.explode()
            self.state.track_players_bombs(self.boom.get_pos())
            self.state.track_treasures(self.boom.get_pos())
            return True
        return False


class EventLogic:
    def __init__(self, _game_state, _game_gui, _game_logic=None, _sound=None):
        self._game_state = _game_state
        self._game_gui = _game_gui
        self._game_logic = _game_logic
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
            if time_tracker.trigger():
                self._game_gui.add_time_tracker(time_tracker)
                self.time_trackers.remove(time_tracker)
                self._game_gui.map.remove_sprite(time_tracker.get_boom())

        event = pygame.event.poll()
        if event.type == MOUSEBUTTONUP:
            if self._game_state.get_state() == "welcome":
                if self._game_gui.new.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("new game")
                    self._game_gui.draw(self._game_state.get_state())
                    pygame.display.update()

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
                self._sound.play_beep()
                self.quit()

            elif event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
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
                char_pos = self._game_gui.characters[0].get_pos()[0]-4, self._game_gui.characters[0].get_pos()[1]
                boom = self._game_gui.create_boom(char_pos)
                self._game_gui.map.add_sprites(boom, "bomb")
                boom_trigger = TimeTracking(2, boom, self._game_state)
                self.time_trackers.append(boom_trigger)
                pygame.display.update()