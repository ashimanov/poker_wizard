import models, db, deal, rules, calc


class LogicException(Exception):
    pass


class App_logic:
    def __init__(self):
        self._game_db = db.GameDB()
        self._game_deal = deal.GameDeal()
        self.rules = rules
        self._game_calc = calc.Calculations()

    # check user input to start a new game
    @staticmethod
    def _validate_start_game(players_names_data):
        if len(players_names_data) < 2:
            raise LogicException('Minimum players is 2.')
        if len(players_names_data) > 12:
            raise LogicException('Maximum players is 12.')
        
    # check user input before beginning a new game round
    @staticmethod
    def _validate_play_round(game, cards, round):
        for card in cards: # checks that cards are posted by user in 2-letter format
            if len(card) > 2 or len(card) < 2:
                raise LogicException('Wrong input format. Please use "5H|QS" format. 2 symbols per card.T for 10.')
            if card[0] not in models.input_card_ranks.keys() or card[1] not in models.input_card_suits.keys(): # checks that card posted exists in deck and no non-existent entries like 1R have been posted by user.
                raise LogicException('Wrong card input. Card does not exist.')
            
        # checks that the user posted correct number of cards for the corresponding round of the game
        if round == 0 and (len(cards) > 2 or len(cards) < 2):
            raise LogicException('Please specify exactly 2 cards for pre-flop round.')
        if round == 1 and (len(cards) > 3 or len(cards) < 3):
            raise LogicException('Please specify exactly 3 cards for the Flop round.')
        if round == 2 and (len(cards) > 1 or len(cards) < 1):
            raise LogicException('Please specify exactly 1 card for the Turn round.')
        if round == 3 and (len(cards) > 1 or len(cards) < 1):
            raise LogicException('Please specify exactly 1 card for the River round.')
            
    # formats game starting data    
    @staticmethod
    def from_raw(players_names: str):
        try:
            players_names_data = players_names.split('|')
            return players_names_data
        except Exception as ex:
            return f'logic exception with from_raw: {ex}'
    
    # creates am instance of the Game class
    @staticmethod
    def create_game(players_names_data: str) -> models.Game:
        try:
            number_of_players = len(players_names_data)# number of players declaired for the game
            number_of_listed_players = 0 # number of players listed for the game
            new_game = models.Game()
            while number_of_players > 0:
                setattr(new_game, 'player'+str(number_of_listed_players + 1), models.Player(players_names_data[number_of_listed_players])) # creates Players (player1, player2 etc) in the instance of the Game (in other words - lists players for the game)
                number_of_players -= 1
                number_of_listed_players += 1
            return new_game
        except LogicException as ex:
            return f'logic exception with create_game: {ex}'
        
    
    # returns player's hand from the specified stored game
    def player_hand(self, _id):
        try:
            return self._game_db.player_hand(int(_id)) # here _id is converted to int type as the dictionary in storage uses integers as keys
        except Exception as ex:
            return f'logic exception with player_hand: {ex}'
    
    # returns a list of finished and active games
    def list_games(self):
        try:
            games = self._game_db.list_games()
            games_list = []
            for game in games.keys():
                games_list.append((f'Game #{game}', 'is active' if games[game].active else 'is over'))
            return games_list
        except Exception as ex:
            return f'logic exception with list_games: {ex}'

    # joins and returns info on how to run the app (from rules.py)
    def print_rules(self):
        try:
            rules_raw = self.rules.rules
            rules = '\n- '.join(rules_raw)
            return rules
        except Exception as ex:
            return f'logic exception with print_rules: {ex}'

    # starts a new game 
    def start_game(self, players_names: str):
        try:
            players_names_data = self.from_raw(players_names) # converts starting string to a list of entries
            self._validate_start_game(players_names_data) # validates starting data
            new_game = self.create_game(players_names_data) # creates a new instance of Game class
            stored_new_game = self._game_db.start_game(new_game) # stores the new game in storage (a database in case of a real app)
            player_hand = self.player_hand(stored_new_game.id) # players hand
            new_game_info = f'\n Game started!!! -- {stored_new_game.round}\n -- http://127.0.0.1:5000/api/v1/game/{stored_new_game.id}/ -X POST -d "2H|KS" -- (your cards) to begin pre-flop round.\n\n Players: {players_names_data}\n Cards in deck: {len(stored_new_game.deck)}/52\n\n Your hand: {player_hand}\n\n {stored_new_game.deck}\n'
            return new_game_info
        except Exception as ex:
            return f'logic exception with start_game: {ex}'

    # returns data on a selected game
    def show_game(self, _id):
        try:
            game = self._game_db.show_game(int(_id)) # here _id is converted to int type as the dictionary in storage uses integers as keys

            # checks game status - active or over
            game_info_raw = [' ', ' ']
            if game.active:
                is_active = 'is active'
            else:
                is_active = 'is over'
            game_info_raw.append(f'Game {is_active}')

            # creates a list of players in the game
            players = [' ', 'Players in the game:', ' ']
            for player in vars(game):
                if 'player' in player:
                    players.append(f' {player}: {getattr(getattr(game, str(player)), "name")}')

            game_info = '\n '.join((game_info_raw + players)) # binds together game status and players for use in the 'return' 
            player_hand = self.player_hand(_id) # gets player's hand from the specified stored game

            return f'\n Game #{_id} info: {game_info}\n\n Your hand: {player_hand}\n Community cards: {game.community_cards}\n Game round: {game.round}\n'

        except Exception as ex:
            return f'logic exception with show_game: {ex}'
        
    def play(self, user_input, _id):
        try:
            game = self._game_db.show_game(int(_id)) # fetches the game from the storage

            # checks if the game is active
            match game.active:
                case False:
                    return f'\n Game #{_id} is over. Please start a new game or select another active game to play.\n'
            
            # formats user_input to a list of strings
            user_input = self.from_raw(user_input) 
            
            # check if it is the last round and sets game.active to False if it is the last round
            if game.round == 3 and game.cards_posted[game.round] == False:
                self._validate_play_round(game, user_input, game.round)
                game.cards_posted[game.round] = True
                game.active = False
                save_result = self._game_db.save_game(game, int(_id))
                return f'\n Your hand: {game.player1.player_hand}.\n Community cards: {game.community_cards}\n\n {self._game_calc.calculate_win_chance(game)}\n'

            
            # if the game round is None it starts the game
            if game.round == None and user_input == ['deal']: # deals cards after getting the ['deal'] command
                return self.play_round(game, _id)
            elif game.round == None and user_input != ['deal']: # asks for the ['deal'] command to begin the pre-flop round
                return f'\nPlease post "deal" command to begin the pre-flop round.\n\n'
            
            # if game has begun it begins following rounds
            elif game.round != None and game.cards_posted[game.round] == True and user_input != ['deal']: # checks if the game has begun (game round != None), player has posted their cards (game.cards_posted[game.round] == True) and user_input != ['deal'] --- and asks to post a correct command ['deal'] to begin the next round
                return f'\nPlease post "deal" command to begin the next round.\n\n Current round: {self.round_name(game.round)}\n'
            elif game.round != None and game.cards_posted[game.round] == True and user_input == ['deal']: # begins the next round if all conditions have been met
                return self.play_round(game, _id)
            
            # assigns the posted cards if the round has been played but cards haven't been assigned yet
            elif game.round != None and game.cards_posted[game.round] == False: # checks if the game has begun (game round != None) and player hasn't posted their cards (game.cards_posted[game.round] == Flase
                self._validate_play_round(game, user_input, game.round) # validates user_input to be playing cards
                game.cards_posted[game.round] = True # changes cards_posted attribute to be True
                save_result = self._game_db.save_game(game, int(_id)) # saves the game 
                return f'\n Your hand: {game.player1.player_hand}.\n Community cards: {game.community_cards}\n\n {self._game_calc.calculate_win_chance(game)}\n\n'
        except Exception as ex:
            return f'logic exception with play: {ex}'
        
    # this function gives rounds clean human readable names  
    def round_name(self, round):
        match round:
            case 0:
                return 'pre-flop round'
            case 1:
                return 'flop round'
            case 2:
                return 'turn round'
            case 3:
                return 'river round'
            
    def set_round(self, game):
        try:
            if game.round == None:
                game.round = 0
                return game
            else:
                game.round += 1
                return game
        except Exception as ex:
            return f'logic exception with set_round: {ex}'
        
    # plays game rounds
    def play_round(self, game, _id):
        try:
            game = self.set_round(game) # sets game round
            round = game.round # identifies the current game round
            game = self._game_deal.deal_cards(game, round)
            save_result = self._game_db.save_game(game, int(_id)) # stores the game in the storage, here _id is converted to int type as the dictionary in storage uses integers as keys. save_game is used to store the game in the storage.
            return f'\n\n The {self.round_name(round)} has started! Game round: {round} ({self.round_name(round)}).\n All players have been dealt 2 cards.\n Your cards: {game.player1.player_hand}\n Community cards: {game.community_cards}\n\n Post the dealt cards to complete {self.round_name(round)}.\n\n Cards still in deck: {len(game.deck)}\n {save_result}\n'
        except Exception as ex:
            return f'logic exception with play_round: {ex}'

    # converts 8C format to tuple like ('Eight', 'Clubs')
    def covert_input_cards(self, cards):
        try:
            dealt_cards = []
            for card in cards:
                full_card = (models.input_card_values[card[0]], models.input_card_values[card[1]])
                dealt_cards.append(full_card)
            return dealt_cards
        except Exception as ex:
            return f'logic exception with covert_input_cards: {ex}'





