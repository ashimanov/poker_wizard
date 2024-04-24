import models




class GameStorage:
    def __init__(self):
        self.id_counter = 0
        self.games = {}

    def player_hand(self, _id):
        try:
            return self.games[_id].player1.player_hand
        except Exception as ex:
            return f'storage exception with player_hand: {ex}'


    # creates a list of stored games, both active and finished
    def list_games(self):
        try:
            return self.games
        except Exception as ex:
            return f'storage failed with list_games: {ex}'

    # counts games, sets an id number to a game instance (initialized with game.id=None by default) and stores a new game in storage
    def start_game(self, pre_flop_round):
        try:
            self.id_counter += 1
            pre_flop_round.id = self.id_counter
            self.games[self.id_counter] = pre_flop_round
            return self.games[self.id_counter]
        except Exception as ex:
            return f'storage failed with start_game: {ex}'

    # fetches and returns game info
    def show_game(self, _id):
        try:
            return self.games[_id]
        except Exception as ex:
            return f'storage exception with show_game: {ex}'

    def play_round(self, _id):
        return self.games[_id]
    
    def save_game(self, game, _id):
        try:
            self.games[_id] = game
            return f'Game # {_id} saved successfully'
        except Exception as ex:
            return f'storage exception with save_game: {ex}'

