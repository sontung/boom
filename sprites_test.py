if __name__ == "__main__":
    import pygame
    import gui
    _gui = gui.GameGUI(None, None)
    sprite = pygame.image.load("assets\images\\female2.png")
    while True:
        sprite.set_clip(pygame.Rect(0+22*9, 0, 22, 30))
        img = sprite.subsurface(sprite.get_clip())
        _gui.display_surface.blit(img, (50, 50))
        pygame.display.update()