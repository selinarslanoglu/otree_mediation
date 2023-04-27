from otree.api import *


doc = """
goodbye
"""


class C(BaseConstants):
    NAME_IN_URL = 'goodbye'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    iban1 = models.StringField(label='Please enter your International Bank Account Number (IBAN).')
    iban2 = models.StringField(label='Please re-enter your International Bank Account Number (IBAN).')
    gender = models.StringField(
        choices=['Male', 'Female', 'Other', 'I prefer not to say.'],
        label='Please select your gender.',
        widget=widgets.RadioSelect
    )
    department = models.StringField(label='Please indicate your field of study.')
    q1 = models.StringField(label='What was your strategy in the game?')
    q2 = models.StringField(label='Do you think communication was helpful?')


# PAGES
class LastPart(Page):
    pass


class Survey(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'gender', 'department']


class PaymentInfo(Page):
    form_model = 'player'
    form_fields = ['iban1', 'iban2']


class WaitForOthers(WaitPage):
    pass


class ThankYou(Page):
    pass


page_sequence = [LastPart, Survey, PaymentInfo, WaitForOthers, ThankYou]
