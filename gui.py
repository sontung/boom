import pygame
import threading


class GameGUI:
    def __init__(self, _game_logic, _game_state):
        pygame.init()
        self.buttons = []  # keeping track of number of buttons according to each scene (state)
        self.state = _game_state
        self.logic = _game_logic
        self.sprite_sheet = pygame.image.load("assets\images\sprites_2.png")
        self.characters = []
        self.window_width = 900
        self.window_height = 600
        self.font_size = 30
        self.x_margin = 78
        self.y_margin = 150
        self.colors = {"white": (255, 255, 255),
                       "black": (41, 36, 33),
                       "navy": (0, 0, 128),
                       "red": (139, 0, 0),
                       "blue": (0, 0, 255),
                       "dark": (3, 54, 73),
                       "yellow": (255, 255, 0),
                       "turquoise blue": (0, 199, 140),
                       "green": (0, 128, 0),
                       "light green": (118, 238, 0),
                       "turquoise": (0, 229, 238)}
        self.tile_color_for_numbers = self.colors["light green"]
        self.text_color_for_numbers = self.colors["navy"]
        self.text_color = self.colors["red"]
        self.bg_color = self.colors["green"]
        self.tile_color = self.bg_color
        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Boom")
        self.font = pygame.font.Font("assets\\fonts\Cutie Patootie Skinny.ttf", self.font_size)
        self.font_bold = pygame.font.Font("assets\\fonts\Cutie Patootie.ttf", self.font_size)
        self.pos = (self.window_width/2, self.window_height/2)  # for configuring game difficulty

    def make_text(self, text, color, bg_color, center):
        """
        Make a text object for drawing
        """
        text_surf = self.font.render(text, True, color, bg_color)
        text_rect = text_surf.get_rect()
        text_rect.center = center
        return text_surf, text_rect

    def draw_map(self, sprite):
        """
        Draw the background
        """
        size = 30
        for index_x in range(0, self.window_width, size):
            for index_y in range(0, self.window_height, size):
                self.display_surface.blit(sprite.get_img(), tuple([index_x, index_y]))

    def create_boom(self, pos):
        return Boom(pos, self.sprite_sheet, {"boom": (120, 0), "explosion": (0, 0)}, self.display_surface)

    def draw(self, state):
        """
        Draw the scene
        """
        self.display_surface.fill(self.bg_color)
        if state == "welcome":
            self.setting = Button('Settings', self.text_color, self.tile_color,
                                  (self.window_width/2, self.window_height/2), self)
            self.new = Button('New Game', self.text_color, self.tile_color,
                              (self.window_width/2, self.window_height/2-60), self)
            self.quit = Button('Quit', self.text_color, self.tile_color,
                               (self.window_width/2, self.window_height/2+180), self)
            self.help = Button('How to play', self.text_color, self.tile_color,
                               (self.window_width/2, self.window_height/2+60), self)
            self.author = Button('About the author', self.text_color, self.tile_color,
                                 (self.window_width/2, self.window_height/2+120), self)
            self.buttons = [self.new, self.setting, self.quit, self.help, self.author]
            self.display_surface.blit(self.setting.get_sr()[0], self.setting.get_sr()[1])
            self.display_surface.blit(self.new.get_sr()[0], self.new.get_sr()[1])
            self.display_surface.blit(self.quit.get_sr()[0], self.quit.get_sr()[1])
            self.display_surface.blit(self.help.get_sr()[0], self.help.get_sr()[1])
            self.display_surface.blit(self.author.get_sr()[0], self.author.get_sr()[1])

        elif state == "new game":
            if not self.characters:
                self.main_character = Character([self.window_width/2, self.window_height/2], self.sprite_sheet, {"up": (240, 0),
                                                                                                              "down": (180, 0),
                                                                                                              "left": (360, 0),
                                                                                                              "right": (300, 0)})
            self.characters = [self.main_character]
            self.buttons = []
            self.draw_map(Sprite(None, self.sprite_sheet, {"down": (30, 0)}))
            self.display_surface.blit(self.main_character.get_img(), tuple(self.main_character.get_pos()))
            #self.display_surface.blit()


class Button:
    def __init__(self, text, color, bg_color, center, _game_gui):
        self.gui = _game_gui
        self.text = text
        self.center = center
        self.color = color
        self.bg_color = bg_color
        self.bold = False
        self.font = self.gui.font
        self.font_bold = self.gui.font_bold
        self.surf = self.font.render(text, True, color, bg_color)
        self.rect = self.surf.get_rect()
        self.rect.center = self.center

    def make_text(self):
        """
        Make a text object for drawing
        """
        if not self.bold:
            text_surf = self.font.render(self.text, True, self.color, self.bg_color)
        else:
            text_surf = self.font_bold.render(self.text, True, self.color, self.bg_color)
        text_rect = text_surf.get_rect()
        text_rect.center = self.center
        return text_surf, text_rect

    def get_rect(self):
        return self.rect

    def get_sr(self):
        return self.surf, self.rect

    def update_sr(self):
        self.surf, self.rect = self.make_text()

    def set_bold(self, pos):
        """
        Highlight the button when the user hovers mouse over
        """
        if self.rect.collidepoint(pos):
            self.bold = True
            self.update_sr()
            self.gui.display_surface.blit(self.surf, self.rect)


class Boom:
    def __init__(self, pos, sheet, loc_in_sheet, surface, extra_explode=0):
        self.pos = pos
        self.sheet = sheet
        self.loc_in_sheet = loc_in_sheet
        self.time_counting = 2000  # the time in ms that the bomb will explode after trigger
        self.surface = surface
        self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["boom"][0], self.loc_in_sheet["boom"][1], 30, 30))
        self.boom_sprite = self.sheet.subsurface(self.sheet.get_clip())
        self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["explosion"][0], self.loc_in_sheet["explosion"][1], 30, 30))
        self.explode_sprite = self.sheet.subsurface(self.sheet.get_clip())
        self.extra_explode = extra_explode  # by default, a boom will explode to 4 sides with the length of 2 tiles

    def get_img(self):
        return self.boom_sprite

    def get_pos(self):
        return self.pos

    def update_pos(self, new_pos):
        self.pos = new_pos

    def leave_boom(self):
        self.surface.blit(self.boom_sprite, self.pos)
        pygame.display.update()

    def explode(self):
        for index in [0, -1, 1, -2, 2]:
            self.surface.blit(self.explode_sprite, tuple([self.pos[0], self.pos[1]+30*index]))
            self.surface.blit(self.explode_sprite, tuple([self.pos[0]+30*index, self.pos[1]]))
        pygame.display.update()


class Sprite:
    def __init__(self, pos, sheet, loc_in_sheet):
        self.sheet = sheet
        self.loc_in_sheet = loc_in_sheet  # a dictionary keeping track of each movement and their sprites
        self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["down"][0], self.loc_in_sheet["down"][1], 30, 30))
        self.img = self.sheet.subsurface(self.sheet.get_clip())
        self.pos = pos

    def get_img(self):
        return self.img


class Character(Sprite):
    def __init__(self, pos, sheet, loc_in_sheet):
        Sprite.__init__(self, pos, sheet, loc_in_sheet)
        self.map = {                      # a dictionary helping choose which img to display according to the movement
            "up":    [[-1], [0]],
            "down":  [[-1], [0]],
            "left":  [[-1], [0]],
            "right": [[-1], [0]]
        }

    def update_img(self, direction):
        self.sheet.set_clip(pygame.Rect(self.loc_in_sheet[direction][0]+30*self.map[direction][0].pop(),
                                        self.loc_in_sheet[direction][1], 30, 30))
        self.img = self.sheet.subsurface(self.sheet.get_clip())

    def update_map(self, direction):
        """
        Helper func to decide which number to add
        then help locating the sprite in the sheet.
        :return:
        """
        number_to_add = self.map[direction][1].pop()
        self.map[direction][0].append(number_to_add)
        if number_to_add == -1:
            self.map[direction][1].append(0)
        else:
            self.map[direction][1].append(-1)

    def get_pos(self):
        return tuple(self.pos)

    def increment_pos(self, direction):
        if direction == "up":
            self.pos[1] -= 15
            self.update_img(direction)
            self.update_map(direction)
        elif direction == "down":
            self.pos[1] += 15
            self.update_img(direction)
            self.update_map(direction)
        elif direction == "left":
            self.pos[0] -= 15
            self.update_img(direction)
            self.update_map(direction)
        elif direction == "right":
            self.pos[0] += 15
            self.update_img(direction)
            self.update_map(direction)