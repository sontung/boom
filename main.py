import pygame
import gui
import state
import event_logic
import sound


if __name__ == "__main__":
    FPS_clock = pygame.time.Clock()
    game_state = state.GameState()
    game_gui = gui.GameGUI(game_state)
    game_sound = sound.Sound()
    game_gui.add_sound(game_sound)
    game_state.set_state("new game")
    game_state.add_gui(game_gui)
    game_state.add_sound(game_sound)
    game_event_handler = event_logic.EventLogic(game_state, game_gui, game_sound)
    game_gui.draw(game_state.get_state())
    pygame.display.update()
    while True:
        game_gui.draw(game_state.get_state())
        game_state.play_sound()
        game_event_handler.event_handler()
        game_state.if_game_over()
        pygame.display.update()
        FPS_clock.tick(30)