from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random

class InputSubjectID(Page):
    form_model = models.Player
    form_fields = ['subject_ID', 'gender', 'age','timeonpage_InputSubjectID']
    def is_displayed(self):
        return self.round_number == 1
    def before_next_page(self):
        self.participant.vars['wrong_math_answers']=0


class MathProblemLevelOfEffort(Page):
    form_model = models.Player
    form_fields = ['problem_difficulty','timeonpage_MathProblemLevelOfEffort']
	
    def before_next_page(self):
        self.player.GetMathProblem(self.player.problem_difficulty)
        self.player.set_group()
        

class MathProblemInput(Page):
    timeout_seconds = 90
    timeout_submission = None
    form_model = models.Player
    form_fields = ['input_answer','timeonpage_MathProblemInput']
    
    def before_next_page(self):
        self.player.CheckIfWrong(self.player.math_problem_ans, self.player.input_answer)
    
    def vars_for_template(self):
        return {'problem': self.player.math_problem}
    

class MathProblemFeedback(Page):
    timeout_seconds = 5
    form_model = models.Player
    form_fields=['timeonpage_MathProblemFeedback']
    
    def vars_for_template(self):
        return {'answer'    : self.player.math_problem_ans,
                'input_ans' : self.player.input_answer,
                'correct' : self.player.math_problem_ans == self.player.input_answer}
  
class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()
    
    # def before_next_page(self):
        # self.player.set_payoff()	


    body_text = "Waiting for other participants to contribute"

class Results(Page):
    form_model = models.Player
    form_fields=['timeonpage_Results']

    #timeout_seconds = 120
    def vars_for_template(self):
      return {
        'is_control': self.group.condition==0
      }
    def before_next_page(self):
        self.player.create_counterfactual_json()

      
# set to a number other than 1 if debugging rest of experiment
instructions_round_number = 1   
  
class Instructions1(Page):
  form_model = models.Player
  form_fields = ['timeonpage_Instructions1']
  def is_displayed(self):
    return self.round_number == instructions_round_number

class Instructions2(Page):
  form_model = models.Player
  form_fields = ['timeonpage_Instructions2']
  def is_displayed(self):
    return self.round_number == instructions_round_number

class Instructions3(Page):
  form_model = models.Player
  form_fields = ['timeonpage_Instructions3']
  def is_displayed(self):
    return self.round_number == instructions_round_number

class Instructions4(Page):
  form_model = models.Player
  form_fields = ['timeonpage_Instructions4']
  def is_displayed(self):
    return self.round_number == instructions_round_number

class InstructionsQuiz(Page):
    form_model=models.Player
    form_fields=['IQ1','IQ2','IQ3','timeonpage_InstructionsQuiz']
    def is_displayed(self):
        return self.round_number == instructions_round_number

class InstructionsQuizFeedback(Page):
    form_model=models.Player
    form_fields=['timeonpage_InstructionsQuizFeedback']
    def is_displayed(self):
        return self.round_number == instructions_round_number
    def vars_for_template(self):
        return {
            '1_correct': self.player.IQ1==4,
            '2_correct': self.player.IQ2==1,
            '3_correct': self.player.IQ3==4
        }


class InstructionsWaitPage(WaitPage):
  body_text = "Waiting for other participants to finish reading instructions"
  def is_displayed(self):
    return self.round_number == instructions_round_number

class GroupingWaitPage(WaitPage):
  body_text = "Waiting for other players...please stand by..."
  group_by_arrival_time = True


class DebriefQuestions(Page):
  form_model = models.Player
  form_fields=['DBQ1','DBQ2','DBQ3','DBQ4','DBQ5','DBQ6','timeonpage_DebriefQuestions1']
  
  def before_next_page(self):
    self.player.CalculateTotalPayoff()
  
  def is_displayed(self):
    return self.round_number == models.Constants.num_rounds
  
  def get_form_fields(self):
    fields=self.form_fields[:(len(self.form_fields)-1)]
    random.shuffle(fields)
    return fields+self.form_fields[(len(self.form_fields)-1):]

class DebriefQuestions2(Page):
  form_model = models.Player
  form_fields=['DB_CF1','DB_CF2','Debrief_OtherComments','timeonpage_DebriefQuestions2']
  
  def before_next_page(self):
    self.player.CalculateTotalPayoff()
  
  def is_displayed(self):
    return self.round_number == models.Constants.num_rounds
  

class Counterfactuals_new(Page):
    form_model = models.Player
    form_fields=['timeonpage_Counterfactuals']
    def is_displayed(self):
        return self.group.condition!=0

# page_sequence = [Counterfactuals_new]

# modify sequence for testing, original seqeuence below
page_sequence = [
	GroupingWaitPage,
	InputSubjectID,
    Instructions1,
    Instructions2,
    Instructions3,
    InstructionsQuiz,
    InstructionsQuizFeedback,
    InstructionsWaitPage,
    MathProblemLevelOfEffort,
    MathProblemInput,
    MathProblemFeedback,
    ResultsWaitPage,
    Results,
    Counterfactuals_new,
    DebriefQuestions,
    DebriefQuestions2
]

# sequence for testing
# page_sequence = [
    # GroupingWaitPage,
    # InputSubjectID,
    # InstructionsWaitPage,
    # MathProblemLevelOfEffort,
    # MathProblemInput,
	# MathProblemFeedback,
    # ResultsWaitPage,
    # Results,
    # Counterfactuals_new,
    # DebriefQuestions,
    # DebriefQuestions2
# ]
