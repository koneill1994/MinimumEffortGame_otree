from minimum_effort_game.math_problem_code import math_sum as mp

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)




author = 'Kevin O\'Neill'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'minimum_effort_game'
    players_per_group = 4
    num_rounds = 10
    min_choice = 1
    max_choice = 7
    base_payment = 1
    scale = 1
    instructions_template = 'public_goods/Instructions.html' # temporary
    min_diff=1
    max_diff=7
    payoffmatrix = [["70",   "",   "",   "",   "",   "",   ""],
                    ["60", "80",   "",   "",   "",   "",   ""],
                    ["50", "70", "90",   "",   "",   "",   ""],
                    ["40", "60", "80","100",   "",   "",   ""],
                    ["30", "50", "70", "90","110",   "",   ""],
                    ["20", "40", "60", "80","100","120",   ""],
                    ["10", "30", "50", "70", "90","110","130"]]
    difficulty_levels = [1,2,3,4,5,6,7]



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    
    min_group = models.CurrencyField()
    max_payoff = models.CurrencyField()
    
    # with help from m_collins:
    def set_payoffs(self):
      
      self.total_contribution = sum([p.problem_difficulty for p in self.get_players()])
      self.min_group = min([p.problem_difficulty for p in self.get_players()])
      self.max_payoff = ((self.min_group - Constants.min_choice) * 10) + 70
      
      for p in self.get_players():
        if p.problem_difficulty == self.min_group:
          p.payoff = self.max_payoff
        else: # presuming the min_group code works right, there won't be anyone below min_group
          p.payoff = self.max_payoff - ((p.problem_difficulty - self.min_group)*10)
          

class Player(BasePlayer):
  
    subject_ID = models.CharField()
    
    problem_difficulty = models.IntegerField(
    min = Constants.min_diff,
    max = Constants.max_diff,
    )
    
    math_problem=models.CharField()
    math_problem_ans=models.FloatField()
    input_answer=models.FloatField(null = True)
    
    def GetMathProblem(self, diff):
      tmp=mp.GenerateEquationAndAnswer(diff)
      self.math_problem = tmp[0]
      self.math_problem_ans = tmp[1]
      return tmp[0]
