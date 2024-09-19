import numpy as np
from otree.api import *


author = 'Yaroslav Rosokha'
doc = """
Post-experimental Questionnaire.
"""


class Constants(BaseConstants):
    name_in_url = 'App02_FinalScreen'
    players_per_group = None
    num_rounds = 1


class Group(BaseGroup):
    pass


class Subsession(BaseSubsession):
    pass


class Player(BasePlayer):
    pass


# FUNCTIONS
# PAGES
class ThankYou(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {'earningsTotal': player.participant.payoff_plus_participation_fee()}


page_sequence = [
    ThankYou,
]
