import time
import event_logic


class GameState:
    """
    The game state
    """
    def __init__(self, _game_sound=None, _game_gui=None):
        self.state = "welcome"
        self.gui = _game_gui
        self.sound = _game_sound
        self.players = []
        self.result = None
        self.time_tracker = None
        self.done_creatingTimeTrackers = False
        self.done_settingGameOver = False

    def play_sound(self):
        if self.state == "welcome":
            self.sound.set_state(0)
            self.sound.play_sound()
        elif self.state == "game over":
            if self.result == "lose":
                self.sound.set_state(3)
                self.sound.play_sound()
            elif self.result == "win":
                self.sound.set_state(9)
                self.sound.play_sound()

    def add_gui(self, _game_gui):
        """
        Provide an access to the game gui object
        """
        self.gui = _game_gui
        self.update_players()

    def add_sound(self, _game_sound):
        self.sound = _game_sound

    def reset(self):
        self.result = None
        self.players = []
        self.time_tracker = None
        self.done_creatingTimeTrackers = False
        self.done_settingGameOver = False

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_result(self, val):
        self.result = val

    def get_result(self):
        return self.result

    def update_players(self):
        if not self.players:
            self.players = [PlayerState(character) for character in self.gui.get_characters()]

    def get_players(self):
        return self.players

    def if_game_over(self):
        for player in self.players:
            if player.get_char().get_tile_pos() == self.gui.map.doors[0].get_pos():
                if not self.done_creatingTimeTrackers:
                    self.time_tracker = event_logic.TimeTracking(2, None)
                    self.time_tracker.set_time(1)
                    self.done_creatingTimeTrackers = True
                if not self.done_settingGameOver and self.time_tracker.time_up():
                    self.set_state("game over")
                    self.set_result("win")
                    self.done_settingGameOver = True
            elif player.get_lives() == 0:
                if not self.done_creatingTimeTrackers:
                    print "creating"
                    self.time_tracker = event_logic.TimeTracking(2, None)
                    self.time_tracker.set_time(3)
                    self.done_creatingTimeTrackers = True
                if not self.done_settingGameOver and self.time_tracker.time_up():
                    self.set_state("game over")
                    self.set_result("lose")
                    self.done_settingGameOver = True

    def if_near_boom(self, player_pos, boom):
        """
        Check to see if the player or something is standing
        near the bomb when it explodes.
        """
        boom_pos = boom.get_pos()
        limit = boom.get_limit_calculated()
        if player_pos[0] == boom_pos[0]:
            if player_pos[1] in range(boom_pos[1]+limit[3]*30, boom_pos[1]+limit[2]*30, 30):
                return True
            else:
                return False
        elif player_pos[1] == boom_pos[1]:
            if player_pos[0] in range(boom_pos[0]+limit[1]*30, boom_pos[0]+limit[0]*30, 30):
                return True
            else:
                return False
        else:
            return False

    def if_near_monster(self, player_pos):
        """
        Check to see if the player jump in a monster.
        """
        player_pos = player_pos[0]-4, player_pos[1]
        for monster in self.gui.monsters:
            if player_pos == tuple(monster.get_pos()):
                return True
        return False

    def track_treasures(self, boom):
        """
        Track the states of treasures in the map.
        """
        treasures = self.gui.map.get_treasures()
        for treasure in treasures:
            if self.if_near_boom(treasure.get_pos(), boom):
                treasure.switch_img()

    def track_players_treasures(self):
        """
        Track the play of players when they eat treasures.
        """
        treasures = self.gui.map.get_treasures()
        for player in self.players:
            for treasure in treasures:
                if treasure.ready_to_eat() and treasure.var_buff != "none":
                    pos = player.get_char().get_pos()[0]-4, player.get_char().get_pos()[1]
                    if pos == treasure.get_pos():
                        treasure.buff(player)
                        self.sound.set_state(4)
                        self.sound.play_sound()
                        self.sound.force_play()
                        self.gui.map.remove_sprite(treasure, "treasure")

    def track_players_monsters(self):
        """
        Track the play of players when they're near monsters.
        """
        for player in self.players:
            if self.if_near_monster(player.get_char().get_pos()) and not player.if_immortal():
                player.update_lives(-1)
                if player.get_lives() == 0:
                    self.sound.set_state(8)
                    self.sound.play_sound()
                    self.sound.force_play()
                else:
                    self.sound.set_state(7)
                    self.sound.play_sound()
                    self.sound.force_play()
                player.set_time_dead()
                self.gui.set_doneBlinkingAnimation(False)

    def track_players_bombs(self, boom):
        """
        Track the play of players when they're near bombs.
        """
        for player in self.players:
            if self.if_near_boom(player.get_char().get_tile_pos(), boom) and not player.if_immortal():
                player.update_lives(-1)
                if player.get_lives() == 0:
                    self.sound.set_state(8)
                    self.sound.play_sound()
                    self.sound.force_play()
                else:
                    self.sound.set_state(7)
                    self.sound.play_sound()
                    self.sound.force_play()
                player.set_time_dead()
                self.gui.set_doneBlinkingAnimation(False)
            for monster in self.gui.monsters:
                if self.if_near_boom(monster.get_pos(), boom):
                    monster.die()
                    self.sound.set_state(5)
                    self.sound.play_sound()
                    self.sound.force_play()
                    self.gui.map.remove_sprite(monster)


class PlayerState:
    """
    The player game state keeping track of all the
    information involved the player.
    """
    def __init__(self, character):
        self.character = character
        self.lives = 3
        self.score = 0
        self.extra_explode = 0
        self.immortal_time = 2  # during this duration, the player is immortal.
        self.time_at_the_moment = 0  # time at the moment the player dies.
        self.ability_open_door = False  # True if this player can open the door.

    def time_up(self):
        if time.time() - self.time_at_the_moment >= self.immortal_time:
            return True
        else:
            return False

    def set_time_dead(self):
        """
        Record the time when the player dies.
        """
        self.time_at_the_moment = time.time()

    def if_immortal(self):
        """
        Return True if the player is still immortal.
        """
        if self.time_up():
            return False
        else:
            return True

    def get_char(self):
        return self.character

    def get_lives(self):
        return self.lives

    def get_extra_explode(self):
        return self.extra_explode

    def get_key(self):
        return self.ability_open_door

    def update_key(self):
        """
        Update the ability to open a door.
        """
        self.ability_open_door = True

    def update_extra_explode(self, amount):
        """
        Increment the player's extra bomb by an amount, his/her bomb
        now explodes broader.
        """
        self.extra_explode += amount

    def update_lives(self, amount):
        """
        Increment the player's lives by an amount, amount can
        be negative.
        """
        self.lives += amount

    def reset_lives(self):
        self.lives = 3

    def get_score(self):
        return self.score

    def update_score(self, amount):
        self.score += amount
