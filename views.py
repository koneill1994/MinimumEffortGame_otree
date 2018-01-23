from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random


survey_round_num=100

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
    timeout_seconds = 25
    def vars_for_template(self):
      return {
      }

class MathProblemLevelOfEffort(Page):
    form_model = models.Player
    form_fields = ['problem_difficulty']

class InputSubjectID(Page):
    form_model = models.Player
    form_fields = ['subject_ID']
    def is_displayed(self):
      return self.round_number == 1

class MathProblemInput(Page):
    timeout_seconds = 90
    form_model = models.Player
    form_fields = ['input_answer']
    
    def vars_for_template(self):
        return {'problem': self.player.GetMathProblem(self.player.problem_difficulty)}
    
class MathProblemInput_template(Page):
    timeout_seconds = 90
    form_model = models.Player
    form_fields = ['input_answer']
    
class MathProblemFeedback(Page):
    timeout_seconds = 5
    form_model = models.Player
    
    def vars_for_template(self):
        return {'answer'    : self.player.math_problem_ans,
                'input_ans' : self.player.input_answer,
                'correct' : self.player.math_problem_ans == self.player.input_answer}

class IndustriousnessScale(Page):
  form_model = models.Player
  
  form_fields = ['indust_1','indust_2','indust_3','indust_4','indust_5','indust_6','indust_7','indust_8','indust_9']
  
  def is_displayed(self):
    return self.round_number == survey_round_num #models.Constants.num_rounds
  
  def get_form_field(self):
    fields = self.form_fields
    random.shuffle(fields)
    return fields
  
class RAS(Page):
  form_model = models.Player
  
  form_fields = ['RAS_01','RAS_02','RAS_03','RAS_04','RAS_05','RAS_06','RAS_07','RAS_08','RAS_09','RAS_10']
  
  def is_displayed(self):
    return self.round_number == survey_round_num #models.Constants.num_rounds
  
  def get_form_field(self):
    fields = self.form_fields
    random.shuffle(fields)
    return fields
    
    
class BSCS(Page):
  form_model = models.Player
  
  form_fields = ['BSCS_01','BSCS_02','BSCS_03','BSCS_04','BSCS_05','BSCS_06','BSCS_07','BSCS_08','BSCS_09','BSCS_10','BSCS_11','BSCS_12','BSCS_13']
  
  def is_displayed(self):
    return self.round_number == survey_round_num #models.Constants.num_rounds
  
  def get_form_field(self):
    fields = self.form_fields
    random.shuffle(fields)
    return fields

class TME(Page):
  form_model = models.Player
  
  form_fields = ['TME_01','TME_02','TME_03','TME_04','TME_05','TME_06','TME_07','TME_08','TME_09',
          'TME_10','TME_11','TME_12','TME_13','TME_14','TME_15','TME_16','TME_17','TME_18','TME_19',
          'TME_20','TME_21','TME_22','TME_23','TME_24','TME_25','TME_26','TME_27','TME_28','TME_29','TME_30']
  
  def is_displayed(self):
    return self.round_number == survey_round_num #models.Constants.num_rounds
  
  def get_form_field(self):
    fields = self.form_fields
    random.shuffle(fields)
    return fields

class TTQ(Page):
  form_model = models.Player
  
  form_fields = ['TTQ_01','TTQ_02','TTQ_03','TTQ_04','TTQ_05','TTQ_06','TTQ_07','TTQ_08','TTQ_09',
        'TTQ_10','TTQ_11','TTQ_12','TTQ_13','TTQ_14','TTQ_15','TTQ_16','TTQ_17','TTQ_18','TTQ_19',
        'TTQ_20','TTQ_21','TTQ_22','TTQ_23','TTQ_24']
  
  def is_displayed(self):
    return self.round_number == survey_round_num #models.Constants.num_rounds
  
  def get_form_field(self):
    fields = self.form_fields
    random.shuffle(fields)
    return fields



class NCS(Page):
  form_model = models.Player
  
  form_fields = ['NCS_01','NCS_02','NCS_03','NCS_04','NCS_05','NCS_06','NCS_07','NCS_08','NCS_09',
        'NCS_10','NCS_11','NCS_12','NCS_13','NCS_14','NCS_15','NCS_16','NCS_17','NCS_18']
  
  def is_displayed(self):
    return self.round_number == survey_round_num #models.Constants.num_rounds
  
  def get_form_field(self):
    fields = self.form_fields
    random.shuffle(fields)
    return fields


class PTIEQ(Page):
  form_model = models.Player
  
  form_fields = ['PTIEQ_01','PTIEQ_02','PTIEQ_03','PTIEQ_04','PTIEQ_05','PTIEQ_06','PTIEQ_07','PTIEQ_08','PTIEQ_09',
      'PTIEQ_10','PTIEQ_11','PTIEQ_12','PTIEQ_13','PTIEQ_14','PTIEQ_15','PTIEQ_16']
  
  def is_displayed(self):
    return self.round_number == survey_round_num #models.Constants.num_rounds
  
  def get_form_field(self):
    fields = self.form_fields
    random.shuffle(fields)
    return fields

### make sure these are all completely randomized


page_sequence = [
    InputSubjectID,
    MathProblemLevelOfEffort,
    MathProblemInput,
    MathProblemFeedback,
    ResultsWaitPage,
    Results,
]

'''
# test sequence

page_sequence = [
    MathProblemLevelOfEffort,
    ResultsWaitPage,
    Results,
]
'''
