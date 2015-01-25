import pygame
import gui
import state
import event_logic

if __name__ == "__main__":
    FPS_clock = pygame.time.Clock()
    game_state = state.GameState()
    game_gui = gui.GameGUI(None, game_state)
    game_event_handler = event_logic.EventLogic(game_state, game_gui)
    game_gui.draw(game_state.get_state())
    pygame.display.update()
    while True:
        game_event_handler.event_handler()