
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'matching_pennies'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 4
    STAKES_POS = cu(50)
    STAKES_NEG = cu(-50)
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    penny_side = models.StringField(choices=[['Heads', 'Heads'], ['Tails', 'Tails']], label='I choose', widget=widgets.RadioSelect)
    wallet = models.CurrencyField(initial=300)
    true_val = models.StringField()
    num_wins = models.IntegerField(initial=0)
def flip(player: Player):
    import random
    import time
    seconds = time.time()
    random.seed(seconds)
    coin_val ='Heads' if random.random() <= 0.5 else 'Tails'
    return coin_val
class Introduction(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        subsession = player.subsession
        return subsession.round_number == 1
class Choice(Page):
    form_model = 'player'
    form_fields = ['penny_side']
    @staticmethod
    def is_displayed(player: Player):
        return True
    @staticmethod
    def vars_for_template(player: Player):
        return dict(player_in_previous_rounds=player.in_previous_rounds())
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        session = player.session
        subsession = player.subsession
        participant = player.participant
        
        player_val = player.penny_side
        player.true_val = flip(player)
        
        change = 0
        if player.true_val == player_val:
            change = C.STAKES_POS
            try:
                player.num_wins = player.in_previous_rounds()[-1].num_wins + 1
            except:
                player.num_wins = 1
        else:
            change = C.STAKES_NEG
            try:
                player.num_wins = player.in_previous_rounds()[-1].num_wins
            except:
                player.num_wins = 0
        
        if subsession.round_number > 1:
        
            prev_wallet_value = player.in_previous_rounds()[-1].wallet
        
        
        
        else:
            prev_wallet_value = cu(300)
        
        new_wallet_value = prev_wallet_value + change
        player.wallet = new_wallet_value
        player.participant.wallet_value = player.wallet
        print(player.participant.wallet_value)
        
        
        
        
        
        
class After_Choice(Page):
    form_model = 'player'
class ResultsSummary(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        player_in_all_rounds = player.in_all_rounds()
        return dict(
            total_payoff=sum([p.payoff for p in player_in_all_rounds]),
            player_in_all_rounds=player_in_all_rounds,
            wallet= participant.wallet_value
        )
page_sequence = [Introduction, Choice, After_Choice, ResultsSummary]