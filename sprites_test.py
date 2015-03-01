if __name__ == "__main__":
    import pygame
    import gui
    _gui = gui.GameGUI(None, None)
    sprite = pygame.image.load("assets\images\\doors.png")
    while True:
        for i in [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]:
            sprite.set_clip(pygame.Rect(0+65*i, 0, 65, 68))
            img = sprite.subsurface(sprite.get_clip())
            _gui.display_surface.blit(img, (80, 80))

            pygame.display.update()