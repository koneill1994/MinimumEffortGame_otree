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

class MathProblemLevelOfEffort(Page):
    timeout_seconds = 15
    form_model = models.Player
    form_fields = ['problem_difficulty']

class MathProblemInput(Page):
    timeout_seconds = 90
    form_model = models.Player
    form_fields = ['input_answer']
    
    def vars_for_template(self):
        return {'problem': self.player.GetMathProblem(player.problem_difficulty)}

'''
page_sequence = [
    Contribute,
    ResultsWaitPage,
    Results,
    MathProblemLevelOfEffort,
    MathProblemInput,
]
'''


page_sequence = [
    MathProblemLevelOfEffort,
    MathProblemInput,
]
