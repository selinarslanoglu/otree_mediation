from otree.api import *

doc = """
game_baseline
"""

PPG = 2


class C(BaseConstants):
    NAME_IN_URL = 'game_baseline'
    PLAYERS_PER_GROUP = PPG
    NUM_ROUNDS = 1
    PAYOFF_MUTUAL_H = 0
    PAYOFF_MUTUAL_L = 75
    PAYOFF_H_WHEN_HL = 200
    PAYOFF_L_WHEN_HL = 50
    CHOICES = [0, 1]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    coordinate = models.BooleanField(
        label="Please choose Action H or Action L.",
        choices=[
            [True, 'L'],
            [False, 'H'],
        ]
    )

    def is_coordinated(self):
        return 'L' if self.coordinate is True else 'H'

    def other_player(self):
        return self.get_others_in_group()[0]


def get_partner(player: Player):
    return player.get_others_in_group()[0]


# PAGES
class Introduction(Page):
    pass


class Chat(Page):
    pass


class Coordination(Page):
    form_model = 'player'
    form_fields = ['coordinate']


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        player_list = group.get_players()
        player_1 = player_list[0]
        player_2 = player_list[1]
        if player_1.coordinate:
            if player_2.coordinate:
                player_1.payoff = C.PAYOFF_MUTUAL_L
                player_2.payoff = C.PAYOFF_MUTUAL_L
            else:
                player_1.payoff = C.PAYOFF_L_WHEN_HL
                player_2.payoff = C.PAYOFF_H_WHEN_HL
        else:
            if player_2.coordinate:
                player_1.payoff = C.PAYOFF_H_WHEN_HL
                player_2.payoff = C.PAYOFF_L_WHEN_HL
            else:
                player_1.payoff = C.PAYOFF_MUTUAL_H
                player_2.payoff = C.PAYOFF_MUTUAL_H


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(partner=get_partner(player))

class ChatPage(Page):
    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)

    @staticmethod
    def live_method(player: Player, data):
        partner = get_partner(player)
        if 'leaveChatOffer' in data:
            leaveChatOffers[player.id_in_group] = data['leaveChatOffer']
            leaveChatOffers[partner.id_in_group] = leaveChatOffers.get(partner.id_in_group, False)
            if all(leaveChatOffer for leaveChatOffer in leaveChatOffers.values()):
                return {0: dict(finished=True)}
        return {partner.id_in_group: data}

leaveChatOffers = dict()

page_sequence = [Introduction, ChatPage, Coordination, ResultsWaitPage, Results]
