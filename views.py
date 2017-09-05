from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    pass


class Contribute(Page):
  
  form_model = models.Player
  form_fields = ['contribution']
  
  
class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "Waiting for other participants to contribute"

class Results(Page):
    def vars_for_template(self):
      return {
      }


page_sequence = [
    Contribute,
    ResultsWaitPage,
    Results
]
