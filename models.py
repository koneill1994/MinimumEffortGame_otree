from minimum_effort_game.math_problem_code import math_problem as mp

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)




author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'minimum_effort_game'
    players_per_group = 4
    num_rounds = 1
    min_choice = 1
    max_choice = 7
    base_payment = 1
    scale = 1
    instructions_template = 'public_goods/Instructions.html' # temporary
    contribution_data=[0]*(max_choice - min_choice)
    min_diff=1
    max_diff=7



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    
    min_group = models.CurrencyField()
    max_payoff = models.CurrencyField()
    

    # with help from m_collins:
    def set_payoffs(self):
      
      self.total_contribution = sum([p.contribution for p in self.get_players()])
      self.min_group = min([p.contribution for p in self.get_players()])
      self.max_payoff = ((self.min_group - Constants.min_choice) * 10) + 70
      
      for p in self.get_players():
        if p.contribution == self.min_group:
          p.payoff = self.max_payoff
        else: # presuming the min_group code works right, there won't be anyone below min_group
          p.payoff = self.max_payoff - ((p.contribution - self.min_group)*10)
          
      for x in range(Constants.max_choice-Constants.min_choice):
        Constants.contribution_data[x] = sum([p.contribution == x+Constants.min_choice for p in self.get_players()])

class Player(BasePlayer):
    contribution = models.CurrencyField(
    min = Constants.min_choice,
    max = Constants.max_choice,
    )
    
    problem_difficulty = models.IntegerField(
    min = Constants.min_diff,
    max = Constants.max_diff,
    )
    
    math_problem=models.CharField()
    math_problem_ans=models.FloatField()
    input_answer=models.FloatField()
    
    def GetMathProblem(diff):
      tmp=mp.GenerateEquationAndAnswer(diff)
      math_problem = tmp[0]
      math_problem_ans = tmp[1]
      return tmp[0]
