# Agent which will run on the EEWA model developed by:
# 
# Kevin O\'Neill
# with theoretical assistance from A_Hough and M_Collins

import numpy, random


class EWA_Agent:
	
	def __init__(self):
		# this is a list which stores the weightings of the payoffs, 
		# which will be used to calculate the choices
		self.weighted_payoffs = [0]*7
		self.choices=range(1,8)
	
		# Free parameters
	
		self.delta = numpy.random.normal(.9,.1) # (mean,sd) forgone payoff parameter parameter. Estimation = .2(0)
		self.rho = .6 # Experience decay parameter. Estimation = .9(.001)
		self.N_prev=0 # initial experience (pregame). 
		self.phi = .7 # attraction decay parameter. Estimation = .21(.17)
		self.lamb = .2 # Sensitivity or ability to discriminate between attractions. Estimation = .49(.09)
		self.attraction_prev = [0]*7 # initial attraction. Should set to starting value that corresponds to first round choice prob --> [8 14.5 18.5 19.5 17.5 13.5 17.5]
	
		# list to hold the attraction values
		self.attraction = self.attraction_prev[:]
		
		#############################################
		#list to hold choice probability
		#################################
		#uniform probability
		#self.choice_prob=[1.0/7]*7
		
		# based on pilot data
		self.choice_prob=[.025,
		.1,
		.2,
		.25,
		.175,
		.075,
		.175]
		
		# initial choice for sanity testing
		self.choice=0 # not possible to get normally
		self.last_payoff=0
	
		
	# payoff function
	def payoff(self,choice,minimum):
		max_payoff = ((minimum - 1) * 10) + 70
		if choice ==minimum:
			return max_payoff
		else:
			if choice < minimum:
				return ((choice - 1) * 10) + 70
			else:
				return max_payoff - (choice-minimum)*10
	
	# this is the function that returns the payoff for each potential choice 
	# (even ones below minimum -- it works out in the math, don't worry about it)			
	# its obsolete now lol don't use this
	def payoff2(self,choice,minimum, min2):
		max_payoff = ((minimum - 1) * 10) + 70
		if choice == minimum:
			return max_payoff
		elif choice < minimum:
			return ((minimum - 1) * 10) + 70
		else:
			if choice < min2:
				return ((min2 - 1) * 10) + 70
			else:
				return (min2-1)*10 + 70 - (choice-min2)*10
		
			
			
	def get_last_choice(self):
		return int(self.choice)
	
	def get_last_payoff(self):
		return int(self.last_payoff)
			
	def get_weighted_payoffs(self):
		return self.weighted_payoffs
		
	def get_attractions(self):
		return self.attraction
		
	def get_choice_prob(self):
		return self.choice_prob
			
	def get_delta(self):
		return self.delta

			
	def make_choice(self):
		self.choice = numpy.random.choice(self.choices,p=self.choice_prob) # is this considering other player's choices? It should only be based on choice probability 
		return int(self.choice)
		
	def update_all_attraction(self, choices, minimum):
	
		self.last_payoff=self.payoff(self.choice, minimum)
	
		# uniques=list(set(choices))
		
		random.shuffle(choices)
		
		for c in choices:
			self.update_attractions(c) # this needs to be changed because it is referencing a replaced functions
			
	def attractions_average(self, minimum, choices): # For each round, this should generate four separate sets of attractions (1-7) for each player's choice treated as a minimum 
		attractions=[]
		
		weighted_payoffs=[0]*7
		attraction=[0]*7
		attraction_out=[0]*7
		
		# for each choice made by a player
		for c in choices: # choices made by all four players
			
			for option in self.choices: # All possible choices (1-7)
				weighted_payoffs[option-1]=self.payoff(option,c)*(self.delta + (1-self.delta)*int(option==self.choice and c==minimum))

			for option in self.choices: # is this right? I have:   Attractions = ( ((phi * N((rprev))) * Attractions(rprev) ) + ( (delta+(1-delta)*I) *  payoff ) ) / Nt;
				attraction[option-1]=(self.phi * self.N_prev * self.attraction_prev[option-1] + weighted_payoffs[option-1])/self.N_current # I think this should this just be under the previous loop?
			
			attractions.append(attraction) # this is replacing all attraction sets with the last set calculated
			
		print(attractions)
		# average together the attraction values. For each round, this should average the four separate sets of attractions
		for i in range(0,len(attraction)):
			for a in attractions:
				attraction_out[i]+=a[i]
			attraction_out[i]/=len(attractions)
			
		return attraction_out
			
	def update_attractions_alex(self, choices, minimum): # For each round, this should update attractions by adding the current round attraction to the previous cumulative attractions over time
		self.N_current=self.rho*self.N_prev+1 # is this right. I have: Nt = rho*Nt(rprev)+1;
		self.attraction=self.attractions_average(minimum,choices)
		
		self.N_prev = self.N_current
		self.attraction_prev=self.attraction[:]
		
		for option in self.choices: # is this right? My code has the equation like this:  ChoiceProb = exp((lambda .* Attractions)) / sum( exp(lambda .* (Attractions)) )
			self.choice_prob[option-1]=numpy.exp(self.lamb*self.attraction[option-1])/sum(numpy.exp( [self.lamb*n for n in self.attraction] ))
		
		self.last_payoff=self.payoff(self.choice, minimum)
			
	# def update_attractions(self, minimum): # This appears to repeat the updating above and may replace values
		
		# for option in self.choices:
			# self.weighted_payoffs[option-1]=self.payoff(option,minimum)*(self.delta + (1-self.delta)*int(option==self.choice and option==minimum))
		   
		# # rho, N_prev are set above
		# self.N_current=self.rho*self.N_prev+1
		# # for each round this is us updating payoffs

		# # phi, attraction_prev are set above

		# for option in self.choices:
			# self.attraction[option-1]=(self.phi * self.N_prev * self.attraction_prev[option-1] + self.weighted_payoffs[option-1])/self.N_current

		# self.N_prev = self.N_current
		# self.attraction_prev=self.attraction[:]

		# for option in self.choices:
			# self.choice_prob[option-1]=numpy.exp(self.lamb*self.attraction[option-1])/sum(numpy.exp( [self.lamb*n for n in self.attraction] ))
	
	def report_state(self):
		
		print("\n\n\n\n")
		
		# print parameters
		print("\nFree parameters")
		print("delta:   "+str(self.delta))
		print("rho:	 "+str(self.rho))
		print("phi:	 "+str(self.phi))
		print("lambda:  "+str(self.lamb))
		
		print("\nPrevious choice")
		print(self.choice)
		
		# isn't recorded anymore when we avg together attractions
		# print("Weighted payoffs:")   
		# print(self.weighted_payoffs)

		print("\nAttractions:")
		print(self.attraction)

		print("\nChoice probabilities:")
		print(self.choice_prob)




k=EWA_Agent()

for n in range(1,2):
	m=k.make_choice()
	k.update_attractions_alex([m,4,5,6],min(m,4))
	k.report_state()

