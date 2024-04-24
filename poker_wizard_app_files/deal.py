import models, random


class DealException(Exception):
    pass

class GameDeal:
    
    
    # ---------------- PRE-FLOP ---------------------

    # removing 'start' from the list to create a 'pure' players' names list:
    @staticmethod
    def make_players_names_list(players_names_data):
        try:
            del players_names_data[0]
            return players_names_data
        except Exception as ex:
            return f'deal error with make_players_names_list: {ex}'


    # deal (x) cards according to the current round
    def deal_cards(self, game, round):
        try:
            match round:
                # pre-flop round, deals 2 cards per player and stores them in game.player.player_hand
                case 0:
                    cards_to_deal = 2
                    while cards_to_deal > 0:
                        for player in vars(game):
                            if 'player' in player:
                                # card = getattr(game, 'deck').pop(random.randrange(0, len(getattr(game, 'deck'))))
                                card = game.deck.pop(random.randrange(0, len(game.deck)))
                                getattr(getattr(game, player), 'player_hand').append(card)
                        cards_to_deal -= 1
                    return game
                
                # flop round, burns the 1st card, then deals three community cards        
                case 1:
                    game.deck.pop(random.randrange(0, len(game.deck))) # burns the first card
                    cards_to_deal = 3
                    while cards_to_deal > 0:
                        game.community_cards.append(game.deck.pop(random.randrange(0, len(game.deck))))
                        cards_to_deal -= 1
                    return game
                
                # turn round, burns the 1st card, then deals one community card
                case 2:
                    game.deck.pop(random.randrange(0, len(game.deck))) # burns the first card
                    cards_to_deal = 1
                    while cards_to_deal > 0:
                        game.community_cards.append(game.deck.pop(random.randrange(0, len(game.deck))))
                        cards_to_deal -= 1
                    return game
                
                # river round, burns the 1st card, then deals one community card
                case 3:
                    game.deck.pop(random.randrange(0, len(game.deck))) # burns the first card
                    cards_to_deal = 1
                    while cards_to_deal > 0:
                        game.community_cards.append(game.deck.pop(random.randrange(0, len(game.deck))))
                        cards_to_deal -= 1
                    return game
                
                case _:
                    return f'Unable to deal cards. Current round: {round}'
        except Exception as ex:
            return f'deal error with deal_cards: {ex}'
        
    def dealer(self, number_of_cards):
        try:
            pass
        except Exception as ex:
            return f'deal exception with dealer: {ex}'

