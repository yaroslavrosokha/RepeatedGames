import copy as cp
import numpy as np
from otree.api import *


author = 'Yaroslav Rosokha'
doc = """
Repeated Game experiment demo based on Dynamic Queue code from Rosokha & Wei (2024 Management Science). 
If you are going to use any of this code, please cite Rosokha, Y. and Wei, C, 2024. Cooperation in Queueing Systems. Management Science.
Runs on otree 5.10.3
"""


class Constants(BaseConstants):
    name_in_url = 'App01_RepeatedGame'
    players_per_group = 2

    # Predrawn sequences of supergame length. Each list is a separate sequence. Config variable in setting determines which on is used.
    sequences = [[2, 3], #<--- for example, sequence 1 has two periods in first repeated game and 3 periods in the second repeated game.
                [3, 2],
                [1, 2]]
    cumulative = [np.roll(np.cumsum(s, dtype=int), 1) for s in sequences]
    num_rounds = int(np.max(cumulative))
    matches = int(len(sequences[0]))
    
    # Payoff_matrix
    payoff_matrices =  [[25, 25], [16, 16]]


class Group(BaseGroup):
    pass


class Subsession(BaseSubsession):
    pass


class Player(BasePlayer):

    matchNumber = models.IntegerField(initial=-1)
    roundNumber = models.IntegerField(initial=-1)
    myChoice = models.IntegerField(initial=-1)
    myPayoff = models.CurrencyField(initial=0)
    roll = models.IntegerField(initial=-1)


    rollHistory = models.StringField(initial="-1")
    roundHistory = models.StringField(initial="-1")
    myChoiceHistory = models.StringField(initial="-1")
    otherChoiceHistory = models.StringField(initial="-1")
    myPayoffHistory = models.StringField(initial="-1")
    otherPayoffHistory = models.StringField(initial="-1")


# FUNCTIONS
def creating_session(subsession: Subsession):

    players = subsession.get_players()
    seq_id = int(subsession.session.config['Sequence']) - 1
    crit_rounds = cp.deepcopy(Constants.cumulative[seq_id])
    crit_rounds[0] = 0
    if subsession.round_number - 1 in crit_rounds:
        subsession.group_randomly() #Create random pairs randomly at the start of each sequence
        for p in players:
            p.roundNumber = 1
            p.matchNumber = int(np.argwhere(crit_rounds == p.round_number - 1)[0][0] + 1)

    else:
        subsession.group_like_round(subsession.round_number - 1)
        for p in players:
            p.roundNumber = p.in_round(p.round_number - 1).roundNumber+1
            p.matchNumber = p.in_round(p.round_number - 1).matchNumber


def init_match(player: Player):
    pass

def init_round(player: Player):
    player.myChoiceHistory = player.in_round(player.round_number - 1).myChoiceHistory
    player.myPayoffHistory = player.in_round(player.round_number - 1).myPayoffHistory
    player.otherChoiceHistory = player.in_round(player.round_number - 1).otherChoiceHistory
    player.otherPayoffHistory = player.in_round(player.round_number - 1).otherPayoffHistory
    player.roundHistory = player.in_round(player.round_number - 1).roundHistory
    player.rollHistory = player.in_round(player.round_number - 1).rollHistory
    player.matchNumber = player.in_round(player.round_number - 1).matchNumber


def update_history(player: Player):
    player.rollHistory += "," + str(player.roll)
    player.roundHistory += "," + str(player.roundNumber)
    player.myChoiceHistory += "," + str(player.myChoice)
    player.myPayoffHistory += "," + str(player.myPayoff)
    for p in player.get_others_in_group():
        player.otherChoiceHistory += "," + str(p.myChoice)
        player.otherPayoffHistory += "," + str(p.myPayoff)

def get_round_outcomes(group: Group):
    
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.myPayoff = Constants.payoff_matrices[p1.myChoice][p2.myChoice]
    p2.myPayoff = Constants.payoff_matrices[p2.myChoice][p1.myChoice]
    p1.payoff = Constants.payoff_matrices[p1.myChoice][p2.myChoice]
    p2.payoff = Constants.payoff_matrices[p2.myChoice][p1.myChoice]

    seq_id = int(group.session.config['Sequence']) - 1
    crit_rounds = Constants.cumulative[seq_id]

    if group.round_number in crit_rounds:
        temp_roll = np.random.choice(list(range(group.session.config['CutoffRoll']+1, group.session.config['MaxRoll']+1)))
        p1.roll = int(temp_roll)
        p2.roll = int(temp_roll)
    else:
        temp_roll = np.random.choice(list(range(1, group.session.config['CutoffRoll']+1)))
        p1.roll = int(temp_roll)
        p2.roll = int(temp_roll)
    update_history(p1)
    update_history(p2)

# PAGES

class beginExperiment(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Matches':10,
            'Matches': int(Constants.matches),
            'PointsPerDollar': int(1.0 / player.session.config['real_world_currency_per_point']),
            'ShowUpFee': int(player.session.config['participation_fee']),
            'CutoffRoll': int(player.session.config['CutoffRoll']),
            'MaxRoll': int(player.session.config['MaxRoll']),
        }

#
class p01_WaitForGroup(WaitPage):
    template_name = 'App01_RepeatedGame/p01_WaitForGroup.html'

    @staticmethod
    def after_all_players_arrive(group: Group):
        seq_id = int(group.session.config['Sequence']) - 1
        crit_rounds = cp.deepcopy(Constants.cumulative[seq_id])
        crit_rounds[0] = 0
        for p in group.get_players():
            if (p.round_number - 1) not in crit_rounds:
                init_round(p)

    @staticmethod
    def vars_for_template(player: Player):
        temp = {
            'rollHistory': player.rollHistory,
            'roundHistory': player.roundHistory,
            'myChoiceHistory': player.myChoiceHistory,
            'otherChoiceHistory': player.otherChoiceHistory,
            'myPayoffHistory': player.myPayoffHistory,
            'otherPayoffHistory': player.otherPayoffHistory,
            'matchNumber': player.matchNumber,
            'CutoffRoll': int(player.session.config['CutoffRoll']),
            'MaxRoll': int(player.session.config['MaxRoll']),
            'myChoice' : player.myChoice,
        }
        return temp



class p02_Round(Page):
    form_model = 'player'
    form_fields = ['myChoice']

    @staticmethod
    def vars_for_template(player: Player):
        temp = {
            'rollHistory': player.rollHistory,
            'roundHistory': player.roundHistory,
            'myChoiceHistory': player.myChoiceHistory,
            'otherChoiceHistory': player.otherChoiceHistory,
            'myPayoffHistory': player.myPayoffHistory,
            'otherPayoffHistory': player.otherPayoffHistory,
            'matchNumber': player.matchNumber,
            'CutoffRoll': int(player.session.config['CutoffRoll']),
            'MaxRoll': int(player.session.config['MaxRoll']),
            'myChoice' : player.myChoice,
        }
        return temp


class p03_WaitForChoice(WaitPage):
    template_name = 'App01_RepeatedGame/p03_WaitForChoice.html'

    @staticmethod
    def after_all_players_arrive(group: Group):
        get_round_outcomes(group)


    @staticmethod
    def vars_for_template(player: Player):

        temp = {
            'rollHistory': player.rollHistory,
            'roundHistory': player.roundHistory,
            'myChoiceHistory': player.myChoiceHistory,
            'otherChoiceHistory': player.otherChoiceHistory,
            'myPayoffHistory': player.myPayoffHistory,
            'otherPayoffHistory': player.otherPayoffHistory,
            'matchNumber': player.matchNumber,
            'myChoice': player.myChoice,
            'CutoffRoll': int(player.session.config['CutoffRoll']),
            'MaxRoll': int(player.session.config['MaxRoll']),
        }
        return temp


class p04_postMatch(Page):
    @staticmethod
    def is_displayed(player: Player):
        seq_id = int(player.session.config['Sequence']) - 1
        crit_rounds = Constants.cumulative[seq_id]
        return player.round_number in crit_rounds

    @staticmethod
    def vars_for_template(player: Player):
        temp = {
            'rollHistory': player.rollHistory,
            'roundHistory': player.roundHistory,
            'myChoiceHistory': player.myChoiceHistory,
            'otherChoiceHistory': player.otherChoiceHistory,
            'myPayoffHistory': player.myPayoffHistory,
            'otherPayoffHistory': player.otherPayoffHistory,
            'matchNumber': player.matchNumber,
            'CutoffRoll': int(player.session.config['CutoffRoll']),
            'MaxRoll': int(player.session.config['MaxRoll']),
            'myChoice' : player.myChoice,

        }
        return temp


page_sequence = [
    beginExperiment,
    p01_WaitForGroup,
    p02_Round,
    p03_WaitForChoice,
    p04_postMatch,
]
