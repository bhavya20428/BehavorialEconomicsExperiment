
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'investment_options'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    OPTION_A = (95, 1000)
    OPTION_B = (75, 200)
    OPTION_C = (50, 50)
    OPTION_D = (25, 25)
    OPTION_E = (0, 5)
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    investment_option = models.StringField(choices=[['A', 'Option A (Risk: 95%, Return: 1000%)'], ['B', 'Option B (Risk: 75%, Return: 200%)'], ['C', 'Option C (Risk: 50%, Return: 50%)'], ['D', 'Option D (Risk: 25%, Return: 25%)'], ['E', 'Option E (Risk: 0%, Return: 5%)']], label='Choose any one of the following investment options:', widget=widgets.RadioSelect)
    wallet = models.CurrencyField()
class Instructions(Page):
    form_model = 'player'
class Choice(Page):
    form_model = 'player'
    form_fields = ['investment_option']
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        import random
        import time
        seed_value = int(time.time())
        random.seed(seed_value)
        
        
        participant.investment_option=player.investment_option
        if(player.investment_option=="A"):
            risk=C.OPTION_A[0]*0.01
            profit=C.OPTION_A[1]*0.01
        elif(player.investment_option=="B"):
            risk=C.OPTION_B[0]*0.01
            profit=C.OPTION_B[1]*0.01
        elif(player.investment_option=="C"):
            risk=C.OPTION_C[0]*0.01
            profit=C.OPTION_C[1]*0.01
        elif(player.investment_option=="D"):
            risk=C.OPTION_D[0]*0.01
            profit=C.OPTION_D[1]*0.01
        elif(player.investment_option=="E"):
            risk=C.OPTION_E[0]*0.01
            profit=C.OPTION_E[1]*0.01
        
        random_number = random.random()
        threshold=1-risk
        if random_number < threshold:
            participant.wallet_value+=participant.wallet_value*cu(profit)
            participant.investment_result="WIN"
            player.wallet=participant.wallet_value
        else:
            participant.wallet_value=0
            participant.investment_result="LOSS"
            player.wallet=participant.wallet_value
        
        
        
        
class Result(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        return dict(
        wallet=participant.wallet_value,
        option=participant.investment_option,
        result=participant.investment_result)
page_sequence = [Instructions, Choice, Result]