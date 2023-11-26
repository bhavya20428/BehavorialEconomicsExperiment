
from otree.api import *
c = cu

doc = '\n\n'
class C(BaseConstants):
    NAME_IN_URL = 'holt_laurey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    STAKES = cu(100)
    OPTION_A_1 = cu(40)
    OPTION_A_2 = cu(32)
    OPTION_B_1 = cu(77)
    OPTION_B_2 = cu(2)
class Subsession(BaseSubsession):
    pass
def creating_session(subsession: Subsession):
    session = subsession.session
    for player in subsession.get_players():
        player.participant.wallet_value=cu(300)
    
    
class Group(BaseGroup):
    pass
def afterArrival(group: Group):
    import random
    import time
    seed_value = int(time.time())
    random.seed(seed_value)
    
    ra=[]
    rn=[]
    rl=[]
    
    for player in group.get_players():
        if(player.participant.category=="RISK_AVERSE"):
            ra.append(player)
        elif(player.participant.category=="RISK_LOVING"):
            rl.append(player)
        else:
            rn.append(player)
    print("Before")
    print(ra)
    print(rn)
    print(rl)
    print()
    random.shuffle(ra)
    random.shuffle(rn)
    random.shuffle(rl)
    
    for i in range(len(ra)):
        if(i%2==0):
            ra[i].participant.allow_for_app_2=True
        else:
            ra[i].participant.allow_for_app_2=False
    
    for i in range(len(rl)):
        if(i%2==0):
            rl[i].participant.allow_for_app_2=True
        else:
            rl[i].participant.allow_for_app_2=False
    
    for i in range(len(rn)):
        if(i%2==0):
            rn[i].participant.allow_for_app_2=True
        else:
            rn[i].participant.allow_for_app_2=False
    print("After")
    print(ra)
    print(rn)
    print(rl)
    print()
    
    
    
class Player(BasePlayer):
    input1 = models.StringField(choices=[['A', 'Option A: $40.00 if throw of die is 1. $32.00 if throw of die is 2-10'], ['B', 'Option B: $77.00 if throw of die is 1. $2.00 if throw of die is 2-10']], label='I choose', widget=widgets.RadioSelect)
    input2 = models.StringField(choices=[['A', 'Option A: $40.00 if throw of die is 1-2. $32.00 if throw of die is 3-10'], ['B', 'Option B:  $77.00 if throw of die is 1-2. $2.00 if throw of die is 3-10']], label='I choose:', widget=widgets.RadioSelect)
    input3 = models.StringField(choices=[['A', 'Option A: $40.00 if throw of die is 1-3. $32.00 if throw of die is 4-10 '], ['B', 'Option B: $77.00 if throw of die is 1-3. $2.00 if throw of die is 4-10 ']], label='I choose: ', widget=widgets.RadioSelect)
    input4 = models.StringField(choices=[['A', 'Option A: $40.00 if throw of die is 1-4. $32.00 if throw of die is 5-10'], ['B', 'Option B: $77.00 if throw of die is 1-4. $2.00 if throw of die is 5-10']], label='I choose: ', widget=widgets.RadioSelect)
    input5 = models.StringField(choices=[['A', 'Option A: $40.00 if throw of die is 1-5. $32.00 if throw of die is 6-10'], ['B', 'Option B: $77.00 if throw of die is 1-5. $2.00 if throw of die is 6-10']], label='I choose: ', widget=widgets.RadioSelect)
    input6 = models.StringField(choices=[['A', 'Option A: $40.00 if throw of die is 1-6. $32.00 if throw of die is 7-10'], ['B', 'Option B: $77.00 if throw of die is 1-6. $2.00 if throw of die is 7-10']], label='I choose: ', widget=widgets.RadioSelect)
    input7 = models.StringField(choices=[['A', 'Option A: $40.00 if throw of die is 1-7. $32.00 if throw of die is 8-10 '], ['B', 'Option B: $77.00 if throw of die is 1-7. $2.00 if throw of die is 8-10 ']], label='I choose:', widget=widgets.RadioSelect)
    input8 = models.StringField(choices=[['A', 'Option A: $40.00 if throw of die is 1-8. $32.00 if throw of die is 9-10.'], ['B', 'Option B: $77.00 if throw of die is 1-8. $2.00 if throw of die is 9-10 ']], label='I choose: ', widget=widgets.RadioSelect)
    input9 = models.StringField(choices=[['A', 'Option A: $40.00 if throw of die is 1-9. $32.00 if throw of die is 10 '], ['B', 'Option B: $77.00 if throw of die is 1-9. $2.00 if throw of die is 10']], label='I choose:', widget=widgets.RadioSelect)
    input10 = models.StringField(choices=[['A', 'Option A: $40.00 if throw of die is 1-10'], ['B', 'Option B: $77.00 if throw of die is 1-10']], label='I choose:', widget=widgets.RadioSelect)
class Intro(Page):
    form_model = 'player'
class Round1(Page):
    form_model = 'player'
    form_fields = ['input1', 'input2']
class Round2(Page):
    form_model = 'player'
    form_fields = ['input3', 'input4']
class Round3(Page):
    form_model = 'player'
    form_fields = ['input5', 'input6']
class Round4(Page):
    form_model = 'player'
    form_fields = ['input7', 'input8']
class Round5(Page):
    form_model = 'player'
    form_fields = ['input9', 'input10']
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        dict={}
        sure_choices=0
        sure_choices_in_exp= 0
        for i in range(1, 11):
            p= i/10.0
            eu_a= p*C.OPTION_A_1 + (1-p)*C.OPTION_A_2
            eu_b= p*C.OPTION_B_1 + (1-p)*C.OPTION_B_2
            if(eu_a>eu_b):
                dict[i]= "A"
                sure_choices_in_exp+=1
            else:
                dict[i]= "B"
        
        
        if(player.input1==dict[1]):
            sure_choices+=1
        
        if(player.input2==dict[2]):
            sure_choices+=1
        
        if(player.input3==dict[3]):
            sure_choices+=1
        
        if(player.input4==dict[4]):
            sure_choices+=1
        
        if(player.input5==dict[5]):
            sure_choices+=1   
        
        if(player.input6==dict[6]):
            sure_choices+=1
        
        if(player.input7==dict[7]):
            sure_choices+=1   
        
        if(player.input8==dict[8]):
            sure_choices+=1
        
        if(player.input9==dict[9]):
            sure_choices+=1
        
        if(player.input10==dict[10]):
            sure_choices+=1
        
        
        participant.safe_options=sure_choices
        
        
        if(sure_choices>sure_choices_in_exp):
            participant.category = "RISK_AVERSE"
        elif(sure_choices<sure_choices_in_exp):
            participant.category = "RISK_LOVING"
        else:
            participant.category = "RISK_NEUTRAL"
        
class WaitForAllPlayers(WaitPage):
    after_all_players_arrive = afterArrival
class ResultsSummary(Page):
    form_model = 'player'
    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        participant = player.participant
        if participant.allow_for_app_2:
            return upcoming_apps[0]
        else:
            return upcoming_apps[1]
page_sequence = [Intro, Round1, Round2, Round3, Round4, Round5, WaitForAllPlayers, ResultsSummary]