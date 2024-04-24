import storage


class GameDB:
    def __init__(self):
        self._storage = storage.GameStorage()

    def player_hand(self, _id):
        try:
            return self._storage.player_hand(_id)
        except Exception as ex:
            return f'db exception with player_hand: {ex}'



    def list_games(self):
        try:
            return self._storage.list_games()
        except Exception as ex:
            return f'db exception with list_games: {ex}'

    def start_game(self, pre_flop_round):
        try:
            return self._storage.start_game(pre_flop_round)
        except Exception as ex:
            return f'db exception with start_game: {ex}'

    def show_game(self, _id):
        try:
            return self._storage.show_game(_id)
        except Exception as ex:
            return f'db exception with show_game: {ex}'

    def play_round(self, _id):
        return self._storage.play_round(_id)
        
    def save_game(self, game, _id):
        try:
            return self._storage.save_game(game, _id)
        except Exception as ex:
            return f'db exception with save_game: {ex}'
    
