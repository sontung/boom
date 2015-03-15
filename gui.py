import pygame
import random
import copy
import event_logic
import map_lvl_1


class GameGUI:
    def __init__(self, _game_logic, _game_state):
        pygame.init()
        self.buttons = []  # keeping track of number of buttons according to each scene (state)
        self.state = _game_state
        self.logic = _game_logic
        self.sprite_sheet = pygame.image.load("assets\images\sprites_sheet_main.png")
        self.monster_sprite = pygame.image.load("assets\images\monster.png")
        self.door_sprite = pygame.image.load("assets\images\doors.png")
        self.male_char_sprite_sheet = pygame.image.load("assets\images\\male.png")
        self.female_char_sprite_sheet = pygame.image.load("assets\images\\female.png")
        self.characters = []
        self.monsters = []
        self.window_width = 870
        self.window_height = 600
        self.information_bar_height = self.window_height / 4  # the height of the information bar
        self.font_size = 30
        self.tile_size = 30
        self.x_margin = 78
        self.y_margin = 150
        self.map = None
        # this list below keeping track of the bombs these are exploding, so their
        # explosion sprites stay for 7 frames.
        self.redundant_time_trackers = []
        self.number_of_monsters = 5
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
        self.bg_color = self.colors["turquoise blue"]
        self.tile_color = self.bg_color
        self.display_surface = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Boom")
        self.font = pygame.font.Font("assets\\fonts\Cutie Patootie Skinny.ttf", self.font_size)
        self.font_bold = pygame.font.Font("assets\\fonts\Cutie Patootie.ttf", self.font_size)
        self.pos = (self.window_width/2, self.window_height/2)  # for configuring game difficulty.
        self.dummy_var = 0  # serves as a way to make blinking animation when the player loses all the lives.
        self.dummy_var1 = 0  # how many frames between each monster to come out.
        self.request_open_door = False  # True if the user press E to open the door.
        self.done_creating_monsters = False
        self.done_blinking_animation = False  # serves as a var to keep track if we've done the blinking animation.

    def make_text(self, text, color, bg_color, center):
        """
        Make a text object for drawing
        """
        text_surf = self.font.render(text, True, color, bg_color)
        text_rect = text_surf.get_rect()
        text_rect.center = center
        return text_surf, text_rect

    def create_boom(self, pos):
        return Boom(pos, self.sprite_sheet, self.display_surface, self, self.state.get_players()[0].get_extra_explode())

    def get_characters(self):
        return self.characters

    def set_doneBlinkingAnimation(self, val):
        self.done_blinking_animation = val

    def if_time_to_release_monster(self):
        """
        Return True if it's time to create a new monster.
        """
        self.dummy_var1 += 1
        if self.dummy_var1 == 20:  # I want new monster coming out after 20 frames.
            self.dummy_var1 = 0
            return True
        else:
            return False

    def set_doneCreatingMonsters(self):
        """
        Set the variable to True if we're done creating monsters.
        """
        if len(self.monsters) == self.number_of_monsters:
            self.done_creating_monsters = True

    def add_time_tracker(self, time_tracker):
        """
        Add redundant time tracker.
        """
        self.redundant_time_trackers.append(time_tracker)

    def set_request_open_door(self):
        self.request_open_door = True

    def draw(self, state):
        """
        Draw the scene.
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
                self.main_character = Character([4, 0], self.male_char_sprite_sheet,
                                                {"up": (66, 0), "down": (0, 0), "right": (132, 0), "left": (132, 0)},
                                                self)
            if not self.map:
                self.map = Map(self, Sprite(None, self.sprite_sheet, {"down": (30, 0)}, self))

                # Adds unbreakable wall sprites
                wall_map = map_lvl_1.WALL_MAP
                for index_y in range(len(wall_map)):
                    for index_x in wall_map[index_y]:
                        if index_x != 0:
                            self.map.add_sprites(Wall((index_x*self.tile_size, index_y*self.tile_size),
                                                      self.sprite_sheet, self), "wall")

                # Adds breakable wall sprites
                none_map = map_lvl_1.NONE_MAP
                for index_y in range(len(none_map)):
                    for index_x in none_map[index_y]:
                        if index_x is not None:
                            self.map.add_sprites(Treasure((index_x*self.tile_size, index_y*self.tile_size),
                                                          self.sprite_sheet, self, "none"), "treasure")

                # Adds extra live treasure sprites
                el_map = map_lvl_1.EL_MAP
                for index_y in range(len(el_map)):
                    for index_x in el_map[index_y]:
                        if index_x is not None:
                            self.map.add_sprites(Treasure((index_x*self.tile_size, index_y*self.tile_size),
                                                          self.sprite_sheet, self, "extra live"), "treasure")

                # Add extra explode treasure sprites
                ee_map = map_lvl_1.EE_MAP
                for index_y in range(len(ee_map)):
                    for index_x in ee_map[index_y]:
                        if index_x is not None:
                            self.map.add_sprites(Treasure((index_x*self.tile_size, index_y*self.tile_size),
                                                          self.sprite_sheet, self, "extra explode"), "treasure")

                # Add key treasure sprite
                key_map = map_lvl_1.KEY_MAP
                for index_y in range(len(key_map)):
                    for index_x in key_map[index_y]:
                        if index_x is not None:
                            self.map.add_sprites(Treasure((index_x*self.tile_size, index_y*self.tile_size),
                                                          self.sprite_sheet, self, "key"), "treasure")

                # Add door sprite
                self.map.add_sprites(Door((420, 210), self.door_sprite, self), "door")

            if not self.done_creating_monsters:
                if self.if_time_to_release_monster():
                    i = len(self.monsters)
                    monster = Monster([420, 210], self.monster_sprite, self,
                                      {"down": (0, 0), "up": (120, 0),"right": (60, 0), "left": (60, 0)}, i % 4)
                    self.monsters.append(monster)
                    self.map.add_sprites(monster, "monster")
                    self.set_doneCreatingMonsters()

            self.characters = [self.main_character]
            self.buttons = []
            self.map.draw_background()
            self.map.draw_sprite()
            self.state.update_players()
            self.state.track_players_treasures()
            for monster in self.monsters[:]:
                if not monster.dead:
                    monster.move()
            if self.request_open_door:
                for door in self.map.doors:
                    door.open_the_door(self.state.get_players()[0])
            self.state.track_players_monsters()

            # I want some sprites stay longer than 1 frame (actually 7 frames) so I add this for loop here
            for time_tracker in self.redundant_time_trackers:
                if time_tracker.time_up():
                    self.redundant_time_trackers.remove(time_tracker)
                else:
                    try:
                        time_tracker.get_sprite().explode()
                    except AttributeError:
                        self.display_surface.blit(time_tracker.get_sprite().get_img(),
                                                  time_tracker.get_sprite().get_pos())

            lives_sur, lives_rect = self.make_text("Lives: %d" % self.state.get_players()[0].get_lives(),
                                                   self.text_color, self.tile_color,
                                                   (60,self.window_height-self.information_bar_height+30))
            self.display_surface.blit(lives_sur, lives_rect)
            if self.state.get_players()[0].get_lives() == 3:
                self.display_surface.blit(self.main_character.get_img(), tuple(self.main_character.get_pos()))
            elif self.state.get_players()[0].get_lives() >= 0:
                if not self.done_blinking_animation:
                    pygame.time.wait(100)
                    if self.dummy_var % 2 == 0:
                        self.display_surface.blit(self.main_character.get_img(), tuple(self.main_character.get_pos()))
                    if self.dummy_var == 5:
                        self.dummy_var = 0
                        self.set_doneBlinkingAnimation(True)
                    self.dummy_var += 1
                else:
                    self.display_surface.blit(self.main_character.get_img(), tuple(self.main_character.get_pos()))
            else:
                pygame.time.wait(100)
                if self.dummy_var % 2 == 0:
                    self.display_surface.blit(self.main_character.get_img(), tuple(self.main_character.get_pos()))
                if self.dummy_var == 9:
                    self.dummy_var = 0
                    self.state.get_players()[0].reset_lives()
                self.dummy_var += 1
        elif state == "game over":
            result = self.state.get_result()
            if result == "win":
                win_sur, win_rect = self.make_text("Congratulations, You won", self.text_color, self.tile_color,
                                                   (self.window_width/2, self.window_height/2))
                self.display_surface.blit(win_sur, win_rect)
            elif result == "lose":
                lose_sur, lose_rect = self.make_text("Sorry, You lost", self.text_color, self.tile_color,
                                                     (self.window_width/2, self.window_height/2))
                self.display_surface.blit(lose_sur, lose_rect)


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
    def __init__(self, pos, sheet, surface, gui, extra_explode=0):
        self.pos = pos
        self.sheet = sheet
        self.loc_in_sheet = {"boom1": (480, 0),
                             "boom2": (510, 0),
                             "center": (0, 50),
                             "up": (30, 50),
                             "down": (90, 50),
                             "right": (150, 50),
                             "left": (60, 50),
                             "row": (120, 50),
                             "col": (180, 50)}
        self.time_counting = 2000  # the time in ms that the bomb will explode after trigger
        self.surface = surface
        self.count = 0  # track of how many frames the explosion sprites have remained
        # I want some nice animations with the bomb so that's why we have two spites for the bomb here.
        self.dummy_var = 0  # serves as an indication to which bomb sprite to be drawn.
        self.prev_dummy_var = 0  # serves as an indication to which bomb sprite to be drawn.
        self.frames = 3  # how many frame between each switch of each sprite.
        self.prev_sprite = 2
        self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["boom1"][0], self.loc_in_sheet["boom1"][1], 30, 30))
        self.boom_sprite1 = self.sheet.subsurface(self.sheet.get_clip())

        self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["boom2"][0], self.loc_in_sheet["boom2"][1], 30, 30))
        self.boom_sprite2 = self.sheet.subsurface(self.sheet.get_clip())

        self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["center"][0], self.loc_in_sheet["center"][1], 30, 30))
        self.center_explode_sprite = self.sheet.subsurface(self.sheet.get_clip())

        self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["up"][0], self.loc_in_sheet["up"][1], 30, 30))
        self.up_explode_sprite = self.sheet.subsurface(self.sheet.get_clip())

        self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["down"][0], self.loc_in_sheet["down"][1], 30, 30))
        self.down_explode_sprite = self.sheet.subsurface(self.sheet.get_clip())

        self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["right"][0], self.loc_in_sheet["right"][1], 30, 30))
        self.right_explode_sprite = self.sheet.subsurface(self.sheet.get_clip())

        self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["left"][0], self.loc_in_sheet["left"][1], 30, 30))
        self.left_explode_sprite = self.sheet.subsurface(self.sheet.get_clip())

        self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["row"][0], self.loc_in_sheet["row"][1], 30, 30))
        self.row_explode_sprite = self.sheet.subsurface(self.sheet.get_clip())

        self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["col"][0], self.loc_in_sheet["col"][1], 30, 30))
        self.col_explode_sprite = self.sheet.subsurface(self.sheet.get_clip())

        self.extra_explode = extra_explode  # by default, a boom will explode to 4 sides with the length of 2 tiles
        self.right = 3 + self.extra_explode  # the right most limit of the explosion
        self.left = -2 - self.extra_explode  # # the left most limit of the explosion
        self.limit = gui.map.decide_limit(self)

    def get_img(self):
        self.dummy_var += 1
        if self.dummy_var - self.prev_dummy_var == self.frames:
            self.prev_dummy_var = self.dummy_var
            if self.prev_sprite == 1:
                self.prev_sprite = 2
                return self.boom_sprite2
            elif self.prev_sprite == 2:
                self.prev_sprite = 1
                return self.boom_sprite1
        else:
            if self.prev_sprite == 1:
                return self.boom_sprite2
            elif self.prev_sprite == 2:
                return self.boom_sprite1

    def get_pos(self):
        return self.pos

    def get_limit_calculated(self):
        """
        Return the limits calculated by Map.
        """
        return self.limit

    def get_limit(self):
        """
        Return the limits of the explosion.
        """
        return self.left, self.right

    def update_pos(self, new_pos):
        self.pos = new_pos

    def explode(self):
        for index in range(self.limit[1], self.limit[0]):
            if index == self.limit[1]:
                self.surface.blit(self.left_explode_sprite, tuple([self.pos[0]+30*index, self.pos[1]]))
            elif index == self.limit[0]-1:
                self.surface.blit(self.right_explode_sprite, tuple([self.pos[0]+30*index, self.pos[1]]))
            else:
                self.surface.blit(self.row_explode_sprite, tuple([self.pos[0]+30*index, self.pos[1]]))
        for index in range(self.limit[3], self.limit[2]):
            if index == self.limit[3]:
                self.surface.blit(self.up_explode_sprite, tuple([self.pos[0], self.pos[1]+30*index]))
            elif index == 0:
                self.surface.blit(self.center_explode_sprite, tuple([self.pos[0], self.pos[1]]))
            elif index == self.limit[2]-1:
                self.surface.blit(self.down_explode_sprite, tuple([self.pos[0], self.pos[1]+30*index]))
            else:
                self.surface.blit(self.col_explode_sprite, tuple([self.pos[0], self.pos[1]+30*index]))
        pygame.display.update()


class Map:
    """
    Keeping track of what can be went through.
    """
    def __init__(self, _game_gui, back_ground_sprite):
        self.gui = _game_gui
        self.walls = []
        self.treasures = []
        self.doors = []
        self.sprites = []
        self.sprite_pos = []
        self.background = back_ground_sprite

    def get_treasures(self):
        """
        Get the list of treasures in the map
        """
        return self.treasures

    def draw_background(self):
        size = 30
        for index_x in range(0, self.gui.window_width, size):
            for index_y in range(0, self.gui.window_height-self.gui.information_bar_height, size):
                self.gui.display_surface.blit(self.background.get_img(), tuple([index_x, index_y]))

    def add_sprites(self, sprite, type_of_sprite):
        """
        Add anything that meant to be appeared in the map like
        walls, treasures, trees, people ... to sprites list
        """
        self.sprites.append(sprite)
        if type_of_sprite == "wall":
            self.walls.append(sprite)
            self.sprite_pos.append(sprite.get_pos())
        elif type_of_sprite == "treasure":
            self.treasures.append(sprite)
            self.sprite_pos.append(sprite.get_pos())
        elif type_of_sprite == "door":
            self.doors.append(sprite)
            self.sprite_pos.append(sprite.get_pos())
        elif type_of_sprite == "bomb":
            self.sprite_pos.append(sprite.get_pos())

    def remove_sprite_pos(self, sprite_pos):
        """
        Remove the sprite_pos so movement through this sprite
        is possible.
        """
        try:
            self.sprite_pos.remove(sprite_pos)
        except ValueError:
            pass

    def remove_sprite(self, sprite, type_of_sprite=None):
        """
        Remove the specified sprite.
        """
        try:
            self.sprites.remove(sprite)
        except ValueError:
            pass
        try:
            self.sprite_pos.remove(sprite.get_pos())
        except ValueError:
            pass
        if type_of_sprite == "wall":
            self.walls.remove(sprite)
        elif type_of_sprite == "treasure":
            self.treasures.remove(sprite)

    def draw_sprite(self):
        """
        Draw anything in the sprites list.
        """
        for sprite in self.sprites:
            self.gui.display_surface.blit(sprite.get_img(), sprite.get_pos())

    def decide_limit(self, boom):
        """
        Decide the limits of the explosion.
        """
        boom_pos = boom.get_pos()
        left, right = boom.get_limit()
        right_limit = right
        left_limit = left
        up_limit = right
        down_limit = left
        for x in range(boom_pos[0], boom_pos[0]+right*30, 30):
            if (x, boom_pos[1]) in self.sprite_pos:
                right_limit = (x-boom_pos[0])/30+1
                break
        for x in range(boom_pos[0], boom_pos[0]+left*30, -30):
            if (x, boom_pos[1]) in self.sprite_pos:
                left_limit = (x-boom_pos[0])/30
                break
        for y in range(boom_pos[1], boom_pos[1]+right*30, 30):
            if (boom_pos[0], y) in self.sprite_pos:
                up_limit = (y-boom_pos[1])/30+1
                break
        for y in range(boom_pos[1], boom_pos[1]+left*30, -30):
            if (boom_pos[0], y) in self.sprite_pos:
                down_limit = (y-boom_pos[1])/30
                break
        return right_limit, left_limit, up_limit, down_limit

    def movement_approve(self, char_pos, direction):
        """
        Approve the movement of the character or monster along that direction
        if it won't pass through any sprites.
        """
        if direction == "up":
            char_pos_after_move = char_pos[0], char_pos[1]-30
        elif direction == "down":
            char_pos_after_move = char_pos[0], char_pos[1]+30
        elif direction == "right":
            char_pos_after_move = char_pos[0]+30, char_pos[1]
        elif direction == "left":
            char_pos_after_move = char_pos[0]-30, char_pos[1]
        for pos in self.sprite_pos:
            if char_pos_after_move == pos:
                return False
        return True


class Sprite:
    def __init__(self, pos, sheet, loc_in_sheet, _game_gui, specific_dim=None):
        self.sheet = sheet
        self.loc_in_sheet = loc_in_sheet  # a dictionary keeping track of each movement and their sprites
        if specific_dim:
            self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["down"][0], self.loc_in_sheet["down"][1],
                                            specific_dim[0], specific_dim[1]))
        else:
            self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["down"][0], self.loc_in_sheet["down"][1], 30, 30))
        self.img = self.sheet.subsurface(self.sheet.get_clip())
        self.pos = pos
        self.gui = _game_gui

    def get_img(self):
        return self.img

    def get_pos(self):
        return self.pos


class Wall(Sprite):
    def __init__(self, pos, sheet, _game_gui, loc_in_sheet={"down": (590, 0)}):
        Sprite.__init__(self, pos, sheet, loc_in_sheet, _game_gui)


class Monster(Sprite):
    def __init__(self, pos, sheet, _game_gui, loc_in_sheet, type_of_monster=0):
        Sprite.__init__(self, pos, sheet, loc_in_sheet, _game_gui)
        self.count = 0  # serves as a var to keep track of how many frames passed
        self.current_direction = "down"  # only change this direction if not able to move further
        self.type_of_monster = type_of_monster  # this var indicates which type of monster (red monster or blue monster)
        self.dead = False
        self.map = {                     # a dictionary helping choose which img to display according to the movement
            "up":    [[0], [1]],
            "down":  [[0], [1]],
            "left":  [[0], [1]],
            "right": [[0], [1]]
        }

    def update_img(self, direction):
        if direction == "right":
            self.sheet.set_clip(pygame.Rect(self.loc_in_sheet[direction][0] + 30*self.map[direction][0].pop(),
                                            self.loc_in_sheet[direction][1] + 28*self.type_of_monster, 30, 28))
            self.img = pygame.transform.flip(self.sheet.subsurface(self.sheet.get_clip()), 1, 0)
        else:
            self.sheet.set_clip(pygame.Rect(self.loc_in_sheet[direction][0] + 30*self.map[direction][0].pop(),
                                            self.loc_in_sheet[direction][1] + 28*self.type_of_monster, 30, 28))
            self.img = self.sheet.subsurface(self.sheet.get_clip())

    def update_map(self, direction):
        """
        Helper func to decide which number to add
        then help locating the sprite in the sheet.
        """
        number_to_add = self.map[direction][1].pop()
        self.map[direction][0].append(number_to_add)
        if number_to_add == 1:
            self.map[direction][1].append(0)
        elif number_to_add == 0:
            self.map[direction][1].append(1)

    def decide_move(self):
        """
        Decide which direction for the monster.
        """
        if self.gui.map.movement_approve(self.pos, self.current_direction) and not self.if_reach_edges():
            return self.current_direction
        else:
            possible_moves = []
            for possible_move in ["up", "left", "down", "right"]:
                if self.gui.map.movement_approve(self.pos, possible_move):
                    possible_moves.append(possible_move)
            self.set_current_direction(random.choice(possible_moves))
            return self.current_direction

    def set_current_direction(self, direction):
        self.current_direction = direction

    def track(self):
        """
        Decide if it's time to move, I don't want the monster
        move too fast.
        """
        self.count += 1
        if self.count == 7:
            self.count = 0
            return True
        else:
            return False

    def if_reach_edges(self):
        """
        Find out if the monster has reached the 4 edges of the window
        indicating a sign that current direction need to be changed.
        """
        if self.current_direction == "up" and self.pos[1] == 0:
            return True
        elif self.current_direction == "down" and self.pos[1] == self.gui.window_height-30-self.gui.information_bar_height:
            return True
        elif self.current_direction == "left" and self.pos[0] == 0:
            return True
        elif self.current_direction == "right" and self.pos[0] == self.gui.window_width-30:
            return True
        else:
            return False

    def move(self):
        """
        Move the monster.
        """
        if self.track():
            direction = self.decide_move()
            # copy.copy prevents the change  in self.pos below
            # also leads to the change in self.previous_pos
            if direction == "up" and self.pos[1] > 0:
                self.pos[1] -= 15
                self.update_img(direction)
                self.update_map(direction)
            elif direction == "down" and self.pos[1] < self.gui.window_height-30-self.gui.information_bar_height:
                self.pos[1] += 15
                self.update_img(direction)
                self.update_map(direction)
            elif direction == "left" and self.pos[0] > 0:
                self.pos[0] -= 15
                self.update_img(direction)
                self.update_map(direction)
            elif direction == "right" and self.pos[0] < self.gui.window_width-30:
                self.pos[0] += 15
                self.update_img(direction)
                self.update_map(direction)

    def die(self):
        """
        Play a nice sprite when a monster dies.
        """
        self.sheet.set_clip(pygame.Rect(0, 112, 30, 28))
        self.img = self.sheet.subsurface(self.sheet.get_clip())
        self.dead = True
        self.gui.monsters.remove(self)
        self.gui.add_time_tracker(event_logic.TimeTracking(2, self))


class Treasure(Sprite):
    def __init__(self, pos, sheet, _game_gui, buff, loc_in_sheet={"down": (560, 0)}):
        Sprite.__init__(self, pos, sheet, loc_in_sheet, _game_gui)
        if buff == "extra live":
            self.loc_in_sheet["secondary"] = (540, 0)
            self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["secondary"][0], self.loc_in_sheet["secondary"][1], 20, 19))
            self.secondary_img = self.sheet.subsurface(self.sheet.get_clip())
        elif buff == "extra explode":
            self.loc_in_sheet["secondary"] = (37, 30)
            self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["secondary"][0], self.loc_in_sheet["secondary"][1], 20, 20))
            self.secondary_img = self.sheet.subsurface(self.sheet.get_clip())
        elif buff == "key":
            self.loc_in_sheet["secondary"] = (0, 80)
            self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["secondary"][0], self.loc_in_sheet["secondary"][1], 20, 20))
            self.secondary_img = self.sheet.subsurface(self.sheet.get_clip())
        elif buff == "none":
            self.loc_in_sheet["secondary"] = (30, 0)
            self.sheet.set_clip(pygame.Rect(self.loc_in_sheet["secondary"][0], self.loc_in_sheet["secondary"][1], 20, 20))
            self.secondary_img = self.sheet.subsurface(self.sheet.get_clip())
        self.var_buff = buff
        self.var_ready_to_eat = False
        self._game_gui = _game_gui

    def switch_img(self):
        """
        Switch to the secondary img if the treasure is near an explosion.
        """
        self.img = self.secondary_img
        self.var_ready_to_eat = True
        self._game_gui.map.remove_sprite_pos(self.get_pos())

    def ready_to_eat(self):
        return self.var_ready_to_eat

    def buff(self, player):
        """
        Make a buff to player.
        """
        if self.var_buff == "extra live":
            player.update_lives(1)
        elif self.var_buff == "extra explode":
            player.update_extra_explode(1)
        elif self.var_buff == "key":
            player.update_key()


class Door(Sprite):
    def __init__(self, pos, sheet, _game_gui, loc_in_sheet={"down": (0, 0)}):
        Sprite.__init__(self, pos, sheet, loc_in_sheet, _game_gui)
        for i in range(1, 11):
            self.loc_in_sheet[str(i)] = (i*315.0/11, 0)
        self.frames = 3  # how many frames each sprite lasts
        self.prev_number = 0  # the previous sprite index in the sheet
        self.completely_open = False

    def set_completely_open(self):
        if self.prev_number == 10:
            self.completely_open = True
            self.gui.map.remove_sprite_pos(self.get_pos())

    def update_img(self, number):
        if self.frames > 0:
            self.frames -= 1
        else:
            self.sheet.set_clip(pygame.Rect(self.loc_in_sheet[number][0], self.loc_in_sheet[number][1], 315.0/11, 30))
            self.img = self.sheet.subsurface(self.sheet.get_clip())
            self.prev_number += 1
            self.frames = 3

    def open_the_door(self, player):
        if player.get_key() and player.get_char().get_tile_pos() == (420, 240):
            if not self.completely_open:
                self.update_img(str(self.prev_number + 1))
                self.set_completely_open()


class Character(Sprite):
    def __init__(self, pos, sheet, loc_in_sheet, _game_gui):
        Sprite.__init__(self, pos, sheet, loc_in_sheet, _game_gui, (22, 30))
        self.map = {                      # a dictionary helping choose which img to display according to the movement
            "up":    [[1], [2]],
            "down":  [[1], [2]],
            "left":  [[1], [2]],
            "right": [[1], [2]]
        }

    def update_img(self, direction):
        if direction == "left":
            self.sheet.set_clip(pygame.Rect(self.loc_in_sheet[direction][0]+22*self.map[direction][0].pop(),
                                            self.loc_in_sheet[direction][1], 22, 30))
            self.img = pygame.transform.flip(self.sheet.subsurface(self.sheet.get_clip()), 1, 0)
        else:
            self.sheet.set_clip(pygame.Rect(self.loc_in_sheet[direction][0]+22*self.map[direction][0].pop(),
                                            self.loc_in_sheet[direction][1], 22, 30))
            self.img = self.sheet.subsurface(self.sheet.get_clip())

    def update_map(self, direction):
        """
        Helper func to decide which number to add
        then help locating the sprite in the sheet.
        """
        number_to_add = self.map[direction][1].pop()
        self.map[direction][0].append(number_to_add)
        if number_to_add == 1:
            self.map[direction][1].append(2)
        elif number_to_add == 2:
            self.map[direction][1].append(0)
        elif number_to_add == 0:
            self.map[direction][1].append(1)

    def map_pos(self, char_pos):
        """
        Map the position of the character to the new position (a new one is a
        multiplication of 30) in the map, then help deciding movement approvement.
        """
        return char_pos[0]-4, char_pos[1]

    def get_pos(self):
        return copy.copy(self.pos)

    def get_tile_pos(self):
        return self.pos[0]-4, self.pos[1]

    def increment_pos(self, direction):
        if self.gui.map.movement_approve(self.get_tile_pos(), direction):
            if direction == "up" and self.pos[1] > 0:
                self.pos[1] -= 10
                self.update_img(direction)
                self.update_map(direction)
            elif direction == "down" and self.pos[1] < self.gui.window_height-30-self.gui.information_bar_height:
                self.pos[1] += 10
                self.update_img(direction)
                self.update_map(direction)
            elif direction == "left" and self.pos[0] > 0:
                self.pos[0] -= 10
                self.update_img(direction)
                self.update_map(direction)
            elif direction == "right" and self.pos[0] < self.gui.window_width-30:
                self.pos[0] += 10
                self.update_img(direction)
                self.update_map(direction)