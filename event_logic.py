import pygame
import sys
from pygame.locals import *


class EventLogic:
    def __init__(self, _game_state, _game_gui, _game_logic=None, _sound=None):
        self._game_state = _game_state
        self._game_gui = _game_gui
        self._game_logic = _game_logic
        self._sound = _sound
        self.movement = {
            K_UP: "up",
            K_DOWN: "down",
            K_RIGHT: "right",
            K_LEFT: "left"
        }

    def quit(self):
        pygame.quit()
        sys.exit()

    def event_handler(self):
        event = pygame.event.poll()

        if event.type == MOUSEBUTTONUP:
            if self._game_state.get_state() == "welcome":
                if self._game_gui.new.get_rect().collidepoint(event.pos):
                    self._game_state.set_state("new game")
                    self._game_gui.draw(self._game_state.get_state())
                    pygame.display.update()

        elif event.type == MOUSEMOTION or event.type == NOEVENT:
            self._game_gui.draw(self._game_state.get_state())
            for button in self._game_gui.buttons:
                button.set_bold(pygame.mouse.get_pos())
            pygame.display.update()

        elif event.type == pygame.QUIT:
            self.quit()

        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                self._sound.play_beep()
                self.quit()

            elif event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                for sprite in self._game_gui.sprites:
                    sprite.increment_pos(self.movement[event.key])
                    self._game_gui.draw("new game")
                    pygame.display.update()
                    pygame.time.wait(100)
                    sprite.increment_pos(self.movement[event.key])
                    self._game_gui.draw("new game")
                    pygame.display.update()