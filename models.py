from minimum_effort_game.math_problem_code import math_sum as mp

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
    num_rounds = 10
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
      
      self.total_contribution = sum([p.problem_difficulty for p in self.get_players()])
      self.min_group = min([p.problem_difficulty for p in self.get_players()])
      self.max_payoff = ((self.min_group - Constants.min_choice) * 10) + 70
      
      for p in self.get_players():
        if p.problem_difficulty == self.min_group:
          p.payoff = self.max_payoff
        else: # presuming the min_group code works right, there won't be anyone below min_group
          p.payoff = self.max_payoff - ((p.problem_difficulty - self.min_group)*10)
          
      for x in range(Constants.max_choice-Constants.min_choice):
        Constants.contribution_data[x] = sum([p.problem_difficulty == x+Constants.min_choice for p in self.get_players()])

class Player(BasePlayer):
  
    subject_ID = models.CharField()
  
    # if all goes well this one will be obsolete
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
    input_answer=models.FloatField(null = True)
    
    def GetMathProblem(self, diff):
      tmp=mp.GenerateEquationAndAnswer(diff)
      self.math_problem = tmp[0]
      self.math_problem_ans = tmp[1]
      return tmp[0]

    # surveys here
    ##############
    
    # industriousness scale
    
    def indust(q):
      return models.IntegerField(
        verbose_name = q,
        choices=[
          [1, 'Never performed this behavior'],
          [2, 'Rarely performed this behavior'],
          [3, 'Sometimes performed this behavior'],
          [4, 'Performed this behavior often'],
          [5, 'Performed this behavior quite often'],
        ],
        widget=widgets.RadioSelect
      )
    
    indust_1 = indust("Work or study long hours")
    indust_2 = indust("Work until I am physically exhausted")
    indust_3 = indust("Work or study on a Friday or Saturday evening")
    indust_4 = indust("Finish a set amount of work before relaxing")
    indust_5 = indust("Volunteer to do things at work that are not part of my job")
    indust_6 = indust("Persist at tasks after meeting setbacks or failures")
    indust_7 = indust("Work extra hard on a project to make sure that it is done right")
    indust_8 = indust("Complete the projects I start")
    indust_9 = indust("Work overtime")


    # Risk Aversion Scale
    def RAS(n,o1,o2):
      return models.IntegerField(
        verbose_name = n,
        choices=[
          [1,"Option 1: "+o1],
          [2,"Option 2: "+o2]
        ],
        widget=widgets.RadioSelect
      )
    
    RAS_01=RAS(
      1,
      "1/10 of winning $2.00 and a 9/10 of winning $1.60",
      "1/10 of winning $3.85 and a 9/10 of winning $0.10"
    )
    RAS_02=RAS(
      2,
      "2/10 of winning $2.00 and a 8/10 of winning $1.60",
      "2/10 of winning $3.85 and a 8/10 of winning $0.10"
    )
    RAS_03=RAS(
      3,
      "3/10 of winning $2.00 and a 7/10 of winning $1.60",
      "3/10 of winning $3.85 and a 7/10 of winning $0.10"
    )
    RAS_04=RAS(
      4,
      "4/10 of winning $2.00 and a 6/10 of winning $1.60",
      "4/10 of winning $3.85 and a 6/10 of winning $0.10"
    )
    RAS_05=RAS(
      5,
      "5/10 of winning $2.00 and a 5/10 of winning $1.60",
      "5/10 of winning $3.85 and a 5/10 of winning $0.10"
    )
    RAS_06=RAS(
      6,
      "6/10 of winning $2.00 and a 4/10 of winning $1.60",
      "6/10 of winning $3.85 and a 4/10 of winning $0.10"
    )
    RAS_07=RAS(
      7,
      "7/10 of winning $2.00 and a 3/10 of winning $1.60",
      "7/10 of winning $3.85 and a 3/10 of winning $0.10"
    )
    RAS_08=RAS(
      8,
      "8/10 of winning $2.00 and a 2/10 of winning $1.60",
      "8/10 of winning $3.85 and a 2/10 of winning $0.10"
    )
    RAS_09=RAS(
      9,
      "9/10 of winning $2.00 and a 1/10 of winning $1.60",
      "9/10 of winning $3.85 and a 1/10 of winning $0.10"
    )
    RAS_10=RAS(
      10,
      "10/10 of winning $2.00 and a 0/10 of winning $1.60",
      "10/10 of winning $3.85 and a 0/10 of winning $0.10"
    )
    
    
    
    def Likert(q):
      return models.IntegerField(
        verbose_name = q,
        choices=[
          [1,"strongly disagree"],
          [2,"disagree"],
          [3,"neither agree nor disagree"],
          [4,"agree"],
          [5,"strongly agree"]
        ],
        widget=widgets.RadioSelectHorizontal
      )
    
    
    
    # brief self control scale
    
    BSCS_01=Likert("I am good at resisting temptation")
    BSCS_02=Likert("I have a hard time breaking bad habits")
    BSCS_03=Likert("I am lazy")
    BSCS_04=Likert("I say inappropriate things")
    BSCS_05=Likert("I do certain things that are bad for me, if they are fun")
    BSCS_06=Likert("I refuse things that are bad for me")
    BSCS_07=Likert("I wish I had more self-discipline")
    BSCS_08=Likert("People would say that I have iron self-discipline")
    BSCS_09=Likert("Pleasure and fun sometimes keep me from getting work done")
    BSCS_10=Likert("I have trouble concentrating")
    BSCS_11=Likert("I am able to work effectively towards long-term goals")
    BSCS_12=Likert("Sometimes I can't stop myself from doing something, even if i know it is wrong")
    BSCS_13=Likert("I often act without thinking through all the alternatives")
    
    
    
    # tolerance of mental effort
    
    def TME(q):
      return models.IntegerField(
        verbose_name = q,
        choices=[
          [1,"definitely not true"],
          [2,"not true"],
          [3,"probably not true"],
          [4,"probably true"],
          [5,"true"],
          [6,"completely true"]
        ],
        widget=widgets.RadioSelectHorizontal
      )
    
    TME_01=TME("I think only as much as I need to")
    TME_02=TME("It is important to ponder upon why things work as they do")
    TME_03=TME("Deliberating about an issue only leads to more mistakes")
    TME_04=TME("It’s hard work to do mental arithmetic")
    TME_05=TME("It’s fun to image what is new and unusual")
    
    TME_06=TME("I would probably define myself as an intellectual")
    TME_07=TME("Trying to solve problems by ones self is a waste of time")
    TME_08=TME("It’s nice not to have to think about things one has learnt before")
    TME_09=TME("I can devote much time to solving problems on my own")
    TME_10=TME("I like tasks that do not require too much brain work")
    
    TME_11=TME("Thinking is the most meaningful thing I can do in my spare time")
    TME_12=TME("I have difficulty imagining new and unfamiliar situations")
    TME_13=TME("I like thinking over possible causes of various events")
    TME_14=TME("I am not exactly a theoretician")
    TME_15=TME("Tasks that require much brainwork (mental effort) are stimulating")
    
    TME_16=TME("I cannot keep pondering upon a problem for long hours")
    TME_17=TME("I prefer working in the same way I have always done")
    TME_18=TME("I often look forward to learning something new")
    TME_19=TME("To think ahead in time is just bothersome")
    TME_20=TME("One makes a better decision if one carefully considers possible options")
    
    TME_21=TME("If something makes me thoughtful I just stop thinking about it")
    TME_22=TME("It annoys me when I need to learn something new")
    TME_23=TME("Intellectual people mean nothing to me")
    TME_24=TME("It is funny to think up new ways to do a job")
    TME_25=TME("It’s nice that things just work so one doesn’t need to wonder why")
    
    TME_26=TME("It’s amusing to speculate what the future holds")
    TME_27=TME("I try to avoid thinking about how and why things occurred")
    TME_28=TME("It is best to make decisions without speculating too much")
    TME_29=TME("I prefer simple mental arithmetic to calculating on paper")
    TME_30=TME("I find it difficult to reason fast under time pressure")
    
    
    
    
    
    
    # Trait Trust Questionnaire
    
    TTQ_01=Likert("I generally have faith in humanity.")
    TTQ_02=Likert("I feel that people are generally reliable.")
    TTQ_03=Likert("I generally trust other people unless they give me a reason not to.")
    TTQ_04=Likert("Most people are basically honest.")
    TTQ_05=Likert("Most people are trustworthy.")
    
    TTQ_06=Likert("Most people are basically good and kind.")
    TTQ_07=Likert("Most people are trustful of others.")
    TTQ_08=Likert("I am trustful.")
    TTQ_09=Likert("Most people will respond in kind when they are trusted by others.")
    TTQ_10=Likert("Hypocrisy is on the increase in our society.")
    
    TTQ_11=Likert("One is better off being cautious when dealing with strangers until they have provided evidence that they are trustworthy.")
    TTQ_12=Likert("Those devoted to unselfish causes are often exploited by others.")
    TTQ_13=Likert("Fear and social disgrace or punishment rather than conscience prevents most people from breaking the law.")
    TTQ_14=Likert("Most experts can be relied upon to tell the truth about the limits of their knowledge.")
    TTQ_15=Likert("Most people tell a lie when they can benefit by doing so.")
    
    TTQ_16=Likert("The judiciary is a place where we can all get unbiased treatment.")
    TTQ_17=Likert("Most people answer public opinion polls honestly.")
    TTQ_18=Likert("Most repairmen will not overcharge, even if they think you are ignorant of their specialty.")
    TTQ_19=Likert("Most people are primarily interested in their own welfare.")
    TTQ_20=Likert("Most students in school would not cheat even if they were sure they could get away with it.")
    
    TTQ_21=Likert("Most people can be counted on to do what they say they will do.")
    TTQ_22=Likert("Most salesmen are honest in describing their products.")
    TTQ_23=Likert("Most elected officials are really sincere in their campaign promises.")
    TTQ_24=Likert("In these competitive times one has to be alert or someone is likely to take advantage of you.")
    
    
    
    
    # Short Form of the Need for Cognition Scale
    
    def NCS(q):
      return models.IntegerField(
        verbose_name = q,
        choices=[
          [1,"extremely uncharacteristic"],
          [2,"somewhat uncharacteristic"],
          [3,"uncertain"],
          [4,"somewhat characteristic"],
          [5,"extremely characteristic"],
        ],
        widget=widgets.RadioSelect
      )
    
    NCS_01=NCS("I would prefer complex to simple problems.")
    NCS_02=NCS("I like to have the responsibility of handling a situation that requires a lot of thinking.")
    NCS_03=NCS("Thinking is not my idea of fun.")
    NCS_04=NCS("I would rather do something that requires little thought than something that is sure to challenge my thinking abilities?")
    NCS_05=NCS("I try to anticipate and avoid situations where there is a likely chance I will have to think in depth about something.")
    
    NCS_06=NCS("I find satisfaction in deliberating hard and for long hours.")
    NCS_07=NCS("I only think as hard as 1 have to.")
    NCS_08=NCS("I prefer to think about small, daily projects to long-term ones?")
    NCS_09=NCS("I like tasks that require little thought once I've learned them?")
    NCS_10=NCS("The idea of relying on thought to make my way to the top appeals to me.")
    
    NCS_11=NCS("I really enjoy a task that involves coming up with new solutions to problems.")
    NCS_12=NCS("Learning new ways to think doesn't excite me very much?")
    NCS_13=NCS("I prefer my life to be filled with puzzles that I must solve.")
    NCS_14=NCS("The notion of thinking abstractly is appealing to me.")
    NCS_15=NCS("I would prefer a task that is intellectual, difficult, and important to one that is somewhat important but does not require much thought.")
    
    NCS_16=NCS("I feel relief rather than satisfaction after completing a task that required a lot of mental effort?")
    NCS_17=NCS("It's enough for me that something gets the job done; I don't care how or why it works?")
    NCS_18=NCS("I usually end up deliberating about issues even when they do not affect me personally.")
    
    
    # Preference for and Tolerance of the Intensity of Exercise Questionnaire
    
    PTIEQ_01=Likert("Feeling tired during exercise is my signal to slow down or stop")
    PTIEQ_02=Likert("I would rather work out at low intensity levels for a long duration than at high intensity levels for a short duration")
    PTIEQ_03=Likert("During exercise, if my muscles begin to burn excessively or if I find myself breathing very hard, it is time for me to ease off")
    PTIEQ_04=Likert("I’d rather go slow during my workout, even if that means taking more time")
    PTIEQ_05=Likert("While exercising, I try to keep going even after I feel exhausted")
    
    PTIEQ_06=Likert("I would rather have a short, intense workout than a long, low intensity workout")
    PTIEQ_07=Likert("I block out the feeling of fatigue when exercising")
    PTIEQ_08=Likert("When I exercise, I usually prefer a slow, steady pace")
    PTIEQ_09=Likert("I’d rather slow down or stop when a workout starts to get tough")
    PTIEQ_10=Likert("Exercising at a low intensity does not appeal to me at all")
    
    PTIEQ_11=Likert("Fatigue is the last thing that affect when I stop a workout; I have a goal and stop only when I reach it")
    PTIEQ_12=Likert("While exercising, I prefer activities that are slow-paced and do not require much exertion")
    PTIEQ_13=Likert("When my muscles start burning during exercise, I usually ease off some")
    PTIEQ_14=Likert("The faster and harder the workout, the more pleasant I feel")
    PTIEQ_15=Likert("I always push through muscle soreness and fatigue when working out")
    
    PTIEQ_16=Likert("Low intensity exercise is boring")
