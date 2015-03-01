import time


class GameState:
    """
    The game state
    """
    def __init__(self, _game_gui=None):
        self.state = "welcome"
        self.gui = _game_gui
        self.players = []

    def add_gui(self, _game_gui):
        """
        Provide an access to the game gui object
        """
        self.gui = _game_gui
        self.update_players()

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def update_players(self):
        if not self.players:
            self.players = [PlayerState(character) for character in self.gui.get_characters()]

    def get_players(self):
        return self.players

    def if_near_boom(self, player_pos, boom_pos):
        """
        Check to see if the player or something is standing
        near the bomb when it explodes.
        """
        if player_pos[0] == boom_pos[0]:
            if player_pos[1] in range(boom_pos[1]-2*30, boom_pos[1]+3*30, 30):
                return True
            else:
                return False
        elif player_pos[1] == boom_pos[1]:
            if player_pos[0] in range(boom_pos[0]-2*30, boom_pos[0]+3*30, 30):
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

    def track_treasures(self, boom_pos):
        """
        Track the states of treasures in the map.
        """
        treasures = self.gui.map.get_treasures()
        for treasure in treasures:
            if self.if_near_boom(treasure.get_pos(), boom_pos):
                treasure.switch_img()

    def track_players_treasures(self):
        """
        Track the play of players when they eat treasures.
        """
        treasures = self.gui.map.get_treasures()
        for player in self.players:
            for treasure in treasures:
                if treasure.ready_to_eat():
                    pos = player.get_char().get_pos()[0]-4, player.get_char().get_pos()[1]
                    if pos == treasure.get_pos():
                        treasure.buff(player)
                        self.gui.map.remove_sprite(treasure, "treasure")

    def track_players_monsters(self):
        """
        Track the play of players when they're near monsters.
        """
        for player in self.players:
            if self.if_near_monster(player.get_char().get_pos()) and not player.if_immortal():
                player.update_lives(-1)
                player.set_time_dead()
                self.gui.set_doneBlinkingAnimation(False)

    def track_players_bombs(self, boom_pos):
        """
        Track the play of players when they're near bombs.
        """
        for player in self.players:
            if self.if_near_boom(player.get_char().get_pos(), boom_pos) and not player.if_immortal():
                player.update_lives(-1)
                player.set_time_dead()
                self.gui.set_doneBlinkingAnimation(False)
            for monster in self.gui.monsters:
                if self.if_near_boom(monster.get_pos(), boom_pos):
                    monster.die()
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
