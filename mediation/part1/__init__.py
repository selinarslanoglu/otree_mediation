from otree.api import *


doc = """
part1
"""


PPG = 2


class C(BaseConstants):
    NAME_IN_URL = 'part1'
    PLAYERS_PER_GROUP = PPG
    NUM_ROUNDS = 1
    PAYOFF_MUTUAL_H = 0
    PAYOFF_MUTUAL_L = 75
    PAYOFF_H_WHEN_HL = 200
    PAYOFF_L_WHEN_HL = 50
    VALIDATION = dict(
        mypayoffifHH = PAYOFF_MUTUAL_H,
        partnerpayoffifLL = PAYOFF_MUTUAL_L,
        mypayoffifHL = PAYOFF_H_WHEN_HL,
        partnerpayoffifLH = PAYOFF_L_WHEN_HL
    )


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    mypayoffifHH = models.IntegerField(
        label="What will be your payoff if both you and the other participant you are matched with choose H?"
    )
    partnerpayoffifLL = models.IntegerField(
        label="What will be the other participant's payoff if both of you choose L?"
    )
    mypayoffifHL = models.IntegerField(
        label="What will be your payoff if you choose H and the other participant you are matched with chooses L?"
    )
    partnerpayoffifLH = models.IntegerField(
        label="What will be the other participant's payoff if you choose L and the other participant you are matched "
              "with chooses H?"
    )
    terminal = models.IntegerField(
        label="Please enter the terminal number."
    )


# PAGES
class Welcome(Page):

    form_model = 'player'
    form_fields = ['terminal']


class Instructions(Page):
    pass


class InstructionsWaitPage(WaitPage):
    wait_for_all_groups = True


class Comprehension(Page):
    errors = []
    form_model = 'player'
    form_fields = ['mypayoffifHH', 'partnerpayoffifLL', 'mypayoffifHL', 'partnerpayoffifLH']

    @staticmethod
    def error_message(self, values):
        Comprehension.errors = []
        error_messages = dict()
        for field_name in C.VALIDATION:
            if values[field_name] != C.VALIDATION[field_name]:
                Comprehension.errors.append(field_name)
                error_messages[field_name] = 'Wrong answer! Please read the instructions again.'

        return error_messages

    @staticmethod
    def js_vars(player):
        return dict(
            errors=Comprehension.errors
        )


class ComprehensionWaitPage(WaitPage):
    wait_for_all_groups = True


page_sequence = [Welcome, Instructions, InstructionsWaitPage, Comprehension, ComprehensionWaitPage]
