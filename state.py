class GameState:
    """
    The pick a number game state
    """
    def __init__(self):
        self.state = "welcome"

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state