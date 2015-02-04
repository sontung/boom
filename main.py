import pygame
import gui
import state
import event_logic

if __name__ == "__main__":
    game_state = state.GameState()
    game_state.set_state("new game")  # for quickly go in the game, for debugging only
    game_gui = gui.GameGUI(None, game_state)
    game_state.add_gui(game_gui)
    game_event_handler = event_logic.EventLogic(game_state, game_gui)
    game_gui.draw(game_state.get_state())
    pygame.display.update()
    while True:
        game_gui.draw(game_state.get_state())
        game_event_handler.event_handler()
        pygame.display.update()