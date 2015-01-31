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
        Check to see if the player is standing
        near the bomb when it explodes
        """
        if player_pos[0] != boom_pos[0] and player_pos[1] != boom_pos[1]:
            return False
        else:
            if player_pos[0] in range(boom_pos[0]-2*30, boom_pos[0]+2*30, 30):
                return True
            elif player_pos[1] in range(boom_pos[1]-2*30, boom_pos[1]+2*30, 30):
                return True
            else:
                return False

    def track_players(self, boom_pos):
        """
        Track the play of players
        """
        self.update_players()
        for player in self.players:
            if self.if_near_boom(player.get_char().get_pos(), boom_pos):
                player.update_lives(-1)


class PlayerState:
    """
    The player game state keeping track of all the
    information involved the player
    """
    def __init__(self, character):
        self.character = character
        self.lives = 3
        self.score = 0

    def get_char(self):
        return self.character

    def get_lives(self):
        return self.lives

    def update_lives(self, amount):
        """
        Increment the player's lives by an amount, amount can
        be negative
        """
        self.lives += amount

    def reset_lives(self):
        self.lives = 3

    def get_score(self):
        return self.score

    def update_score(self, amount):
        self.score += amount