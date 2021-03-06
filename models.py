from minimum_effort_game.math_problem_code import math_sum as mp

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random, json


author = 'Kevin O\'Neill'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'minimum_effort_game'
    players_per_group = 4
    num_rounds = 20
    min_choice = 1
    max_choice = 7
    participation_fee = 3
    scale = .00076923
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

    # counterfactuals conditions
    
    # 0: control no counterfactuals

    # 1: upward: +1 and +2 for min and own_choice
    # 2: downward: -1 and -2 for min and own_choice
    # 3: bidirectional: -1 and +1 for min and own_choice
	
	# modifiy condition for testing (original is (0,4))
    condition=models.IntegerField(initial=random.randrange(0,1))
    
    #debug
    # condition=models.IntegerField(initial=2)
    
    total_contribution = models.IntegerField()
    
    min_group = models.IntegerField()
    max_payoff = models.IntegerField()
    
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
    
    wrong_math_answers=models.IntegerField(initial=0)
    
    payment=models.FloatField()
        
    subject_ID = models.CharField()
    
    gender = models.CharField(
      choices=["Male","Female","Non-binary/third gender","Prefer not to say"]
    )
    
    age=models.IntegerField(
      min=18,
      max=120,
      blank=True
    )
    
    problem_difficulty = models.IntegerField(
        min = Constants.min_diff,
        max = Constants.max_diff,
    )
    
    math_problem=models.CharField()
    math_problem_ans=models.FloatField()
    input_answer=models.FloatField(null = True)
        
    mturk_group_list=models.CharField()
		
    def set_group(self):
        g_id=[]
        for p in self.group.get_players():
            g_id.append(p.subject_ID)
            self.mturk_group_list=json.dumps(g_id)
        
    def calc_payoff(self,choice,minimum):
        max_payoff = ((minimum - 1) * 10) + 70
        if choice ==minimum:
            return max_payoff
        else:
            if choice < minimum:
                return ((choice - 1) * 10) + 70
            else:
                return max_payoff - (choice-minimum)*10
            
        
    def CheckIfWrong(self, ans, p_ans):
      if ans != p_ans:
        self.participant.vars['wrong_math_answers']+=1
        self.wrong_math_answers=self.participant.vars['wrong_math_answers']

    
	# Alex Hough modification to self.payment
    def CalculateTotalPayoff(self):
      # hope rewriting this doesn't cause problems
      self.payment = float((self.participant.payoff-(self.participant.vars['wrong_math_answers']*130))/1300.0)
	    
    
    def GetMathProblem(self, diff):
      tmp=mp.GenerateEquationAndAnswer(diff)
      self.math_problem = tmp[0]
      self.math_problem_ans = tmp[1] 
      return tmp[0]
      
    def GetCounterfactualCount(self):
      Counterfactual_count = int(self.problem_difficulty-1>0)+int(self.problem_difficulty+1<8)+int(group.min_group+1<8)
      
    # counterfactuals
    
    # 0: control no counterfactuals

    # 1: upward: +1 and +2 for min and own_choice
    # 2: downward: -1 and -2 for min and own_choice
    # 3: bidirectional: -1 and +1 for min and own_choice
    
    def counterfactual_format(self):
        if self.group.condition==1:
            return [1,2]
        elif self.group.condition==2:
            return [-1,-2]
        elif self.group.condition==3:
            return [-1,1]
        else:
            return []
    
    counterfactual_json=models.CharField(initial="[]")
    
    def create_counterfactual_json(self):
        json_list=[]
        for cf in self.counterfactual_format():
            if(self.problem_difficulty+cf>0 and 
            self.problem_difficulty+cf<8):
                # set minimum to own choice if choice<minimum
                if(self.problem_difficulty+cf<self.group.min_group):
                    json_list.append([
                        self.problem_difficulty+cf,
                        self.problem_difficulty+cf,
                        self.calc_payoff(
                            self.problem_difficulty+cf,
                            self.problem_difficulty+cf
                        )
                    ])
                else:
                    json_list.append([
                        self.problem_difficulty+cf,
                        self.group.min_group,
                        self.calc_payoff(
                            self.problem_difficulty+cf,
                            self.group.min_group
                        )
                    ])
            
            if(self.group.min_group+cf>0 and 
            self.group.min_group+cf<8):
                # set own choice to minimum if minimum>choice
                if(self.problem_difficulty<self.group.min_group+cf):
                    json_list.append([
                        self.group.min_group+cf,
                        self.group.min_group+cf,
                        self.calc_payoff(
                            self.group.min_group+cf,
                            self.group.min_group+cf
                        )
                    ])
                else:
                    json_list.append([
                        self.problem_difficulty,
                        self.group.min_group+cf,
                        self.calc_payoff(
                            self.problem_difficulty,
                            self.group.min_group+cf
                        )
                    ])
            
        self.counterfactual_json=str(json.dumps(json_list))
        

    # new plan
    # calculate counterfactuals based on condition
    # send counterfactuals to page in json format
    # i.e. [[own_choice, group_min, payoff]]

    # on the counterfactual page:
    # js which copies the table there and makes duplicates
    # json.length-1 times
    # so that we have as many tables as counterfactuals
    # style each based on json data
      
    Counterfactual_count=models.IntegerField()


    timeonpage_InputSubjectID=models.FloatField(blank=True)
    timeonpage_Instructions1=models.FloatField(blank=True)
    timeonpage_Instructions2=models.FloatField(blank=True)
    timeonpage_Instructions3=models.FloatField(blank=True)
    timeonpage_InstructionsQuiz=models.FloatField(blank=True)
    timeonpage_InstructionsQuizFeedback=models.FloatField(blank=True)
    timeonpage_MathProblemLevelOfEffort=models.FloatField(blank=True)
    timeonpage_MathProblemInput=models.FloatField(blank=True)
    timeonpage_MathProblemFeedback=models.FloatField(blank=True)
    timeonpage_Results=models.FloatField(blank=True)
    timeonpage_Counterfactuals=models.FloatField(blank=True)
    timeonpage_DebriefQuestions1=models.FloatField(blank=True, verbose_name="")
    timeonpage_DebriefQuestions2=models.FloatField(blank=True, verbose_name="")

    
    # instructions quiz
    
    IQ1=models.IntegerField(
        verbose_name="What determines your payoff each round?",
        choices=[
            [1,"Your own choice"],
            [2,"Other players choices"],
            [3,"The minimum"],
            [4,"Your choice and the minimum"],
        ],
        widget=widgets.RadioSelect
    )
    
    IQ2=models.IntegerField(
        verbose_name="How would you get the lowest payoff of all players?",
        choices=[
            [1,"Choosing higher effort than other players"],
            [2,"Choosing lower effort than other players"],
            [3,"You and other players choosing lower effort together"],
            [4,"You and other players choosing higher effort together"],
        ],
        widget=widgets.RadioSelect
    )
    
    IQ3=models.IntegerField(
        verbose_name="How would you get the best possible payoff?",
        choices=[
            [1,"Choosing higher effort than other players"],
            [2,"Choosing lower effort than other players"],
            [3,"You and other players choosing lower effort together"],
            [4,"You and other players choosing higher effort together"],
        ],
        widget=widgets.RadioSelect
    )
    
    
    
    # debrief questions

    def Likert7(q):
      return models.IntegerField(
        verbose_name = q,
        choices=[
          [1,"very strongly disagree"],
          [2,"strongly disagree"],
          [3,"disagree"],
          [4,"neither agree nor disagree"],
          [5,"agree"],
          [6,"strongly agree"],
          [7,"very strongly agree"]
        ],
        widget=widgets.RadioSelect
      )
    
    DBQ1=Likert7("I didn't want to have to do a hard math problem")
    DBQ2=Likert7("I wanted a challenging math problem")
    DBQ3=Likert7("I wanted to maximize my own payoff")
    DBQ4=Likert7("I didn't want to seem self-centered")
    DBQ5=Likert7("I wanted to be a team player")
    DBQ6=Likert7("I wanted to see what would happen")
    
    DB_CF1=models.IntegerField(
        verbose_name="What did the counterfactual statements after the results give you information about?",
        choices=[
            [1,"Outcomes for higher choices"],
            [2,"Outcomes for lower choices"],
            [3,"Outcomes for both higher and lower choices"],
			[4,"Outcome of the current round"],
            [5,"I don’t know"]
        ],
        widget=widgets.RadioSelect
    )
    DB_CF2 = models.TextField(verbose_name="Did the counterfactuals influence your choices during the game? How?")
    
    
    Debrief_OtherComments = models.TextField(blank=True, 
      verbose_name='Are there any other comments you would like to share about the task you just did?')
    


