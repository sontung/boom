if __name__ == "__main__":
    import pygame
    import gui
    _gui = gui.GameGUI(None, None)
    sprite = pygame.image.load("assets\images\\sprites_sheet_main.png")
    while True:
        sprite.set_clip(pygame.Rect(0, 50, 30, 30))
        img = sprite.subsurface(sprite.get_clip())
        _gui.display_surface.blit(img, (80, 80))

        sprite.set_clip(pygame.Rect(120, 50, 30, 30))
        img = sprite.subsurface(sprite.get_clip())
        _gui.display_surface.blit(img, (50, 80))
        _gui.display_surface.blit(img, (110, 80))

        sprite.set_clip(pygame.Rect(180, 50, 30, 30))
        img = sprite.subsurface(sprite.get_clip())
        _gui.display_surface.blit(img, (80, 50))
        _gui.display_surface.blit(img, (80, 110))

        sprite.set_clip(pygame.Rect(30, 50, 30, 30))
        img = sprite.subsurface(sprite.get_clip())
        _gui.display_surface.blit(img, (80, 20))

        sprite.set_clip(pygame.Rect(60, 50, 30, 30))
        img = sprite.subsurface(sprite.get_clip())
        _gui.display_surface.blit(img, (20, 80))

        sprite.set_clip(pygame.Rect(90, 50, 30, 30))
        img = sprite.subsurface(sprite.get_clip())
        _gui.display_surface.blit(img, (80, 140))

        sprite.set_clip(pygame.Rect(150, 50, 30, 30))
        img = sprite.subsurface(sprite.get_clip())
        _gui.display_surface.blit(img, (140, 80))
        pygame.display.update()