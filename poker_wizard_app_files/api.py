from flask import Flask, request
import logic

app = Flask(__name__)

_app_logic = logic.App_logic()

class ApiException(Exception):
    pass

API_ROOT = '/api/v1'
GAME_ROOT = API_ROOT + '/game'


# get a list of finished and active games
@app.route(GAME_ROOT + '/', methods=['GET'])
def list_games():
    try:
        games_list = _app_logic.list_games()
        return f'\n{games_list}\n'
    except Exception as ex:
        return f'api exception, could not list_games: {ex}', 404


# get info on how to play and game rules
@app.route(GAME_ROOT + '/rules/', methods=['GET'])
def print_rules():
    try:
        rules = _app_logic.print_rules()
        return rules
    except Exception as ex:
        return f'api exception, could not print rules: {ex}', 404


# start a new game
@app.route(GAME_ROOT + '/', methods=['POST'])
def start_game():
    try:
        players_names = request.get_data().decode('utf-8')
        new_game = _app_logic.start_game(players_names)
        return new_game
    except Exception as ex:
        return f'api exception failed to start_game: {ex}', 404
    
# play the next round of the game
@app.route(GAME_ROOT + '/<_id>/', methods=['POST'])
def play(_id: str):
    try:
        user_input = request.get_data().decode('utf-8') # variable name "user_input" is used as this input will vary from cards to "deal" command and no other name was condidered suitable
        game = _app_logic.play(user_input, _id)
        return game
    except Exception as ex:
        return f'api exception failed to start_game: {ex}', 404


# get info on a particular ghame
@app.route(GAME_ROOT + '/<_id>/', methods=['GET'])
def show_game(_id: str):
    try:
        game = _app_logic.show_game(_id)
        return game
    except Exception as ex:
        return f'api exception failed to show_game: {ex}'



