if __name__ == "__main__":
    import pygame
    import gui
    _gui = gui.GameGUI(None, None)
    sprite = pygame.image.load("assets\images\\monster.png")
    while True:
        sprite.set_clip(pygame.Rect(0, 0, 30, 30))
        img = sprite.subsurface(sprite.get_clip())
        _gui.display_surface.blit(img, (80, 80))

        pygame.display.update()