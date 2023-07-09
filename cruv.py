import random
import time

class Player:
	def __init__(self, name, bowling, batting, fielding, running, experience, age, runs = 0, matches= 0, wickets = 0):
		self.name = name
		self.bowling, self.batting, self.fielding = bowling, batting, fielding
		self.running, self.experience, self.age = running, experience, age
		self.runs, self.matches, self.wickets = runs, matches, wickets
		self.average = (self.runs / self.matches) if self.matches > 0 else 0 
		self.isplaying = False

	#average stats of a player determines its postion in the team
	def average_stats(self):
		return sum([self.bowling, self.batting, self.fielding, self.experience, self.running]) / 5

	def get_stats(self):
		print(f"Name: {self.name}\nBatting: {self.batting}\nBowling: {self.bowling}\nMatches: {self.matches}\nAge: {self.age}\nRuns: {self.runs}\nWickets: {self.wickets}")

class Team:
	def __init__(self, name, players):
		self.name = name
		self.players = players

	def set_captain(self, captain):
		self.captain = captain

	def set_batting_order(self):
		self.batting_order = sorted(self.players, key = lambda x: x.average_stats(), reverse = True)

	def next_to_bat(self):
		return self.batting_order.pop(1)

	def next_to_bowl(self):
		return random.choice(self.players)

class Field:
	def __init__(self, field_size, fan_ratio, pitch_condition, home_advantage):
		self.field_size, self.pitch_condition = field_size, pitch_condition
		self.fan_ratio, self.home_advantage = fan_ratio, home_advantage

	#defining which side has most probability of performing better using field details
	def benefit(self):
		if self.field_size in ['small', 'medium'] and self.fan_ratio > 0.5 or self.pitch_condition == "wet" and self.home_advantage > 0.5:
			return "bat"
		return "bowl"

class Umpire:
	def __init__(self, teams, field):
		self.teams = teams
		self.field = field
		self.scores = {teams[0]: 0, teams[1]:0}
		self.wickets = {teams[0]: 0, teams[1]:0}
		self.overs = 0
		self.innings = 1

	def commentary(self):
		batting_team = self.teams[0].name
		bowling_team = self.teams[1].name
		batter= self.batter.name
		bowler = self.bowler.name
		score= self.scores[self.batting_team]
		wickets = self.wickets[self.batting_team]
		overs = self.overs
		print(f"\n{batter} on strike. {bowler} bowling")
		print(f"{batting_team}: {score}/{wickets} in {overs:.1f} overs")
		
	def calculate_probabilities(self, player):
		benefit = self.field.benefit()

		if benefit == 'bat' and player.batting >= player.bowling:
			return random.randint(6, 10)
		elif benefit == 'bat' and player.batting < player.bowling:
			return random.randint(0, 5)
		elif benefit == 'bowl' and player.bowling >= player.batting:
			return random.randint(5, 10)
		else:
			return random.randint(0,6)

	def simulate_innings(self):
		self.batting_team = self.teams[0]
		self.bowling_team = self.teams[1]
		self.batter = self.batting_team.next_to_bat()
		self.batter.matches += 1
		count = 0
		while self.overs < 2: #number of overs(can be set manually)
			count += 1
			#determines who comes next to bowl
			self.bowler = self.bowling_team.next_to_bowl()
			if not self.bowler.isplaying:
				self.bowler.isplaying = True
				self.bowler.matches += 1

			for _ in range(6):
				#calculate which player has best probability to suceed
				batting_prob = self.calculate_probabilities(self.batter)
				bowling_prob = self.calculate_probabilities(self.bowler)

				#based on probability either batter is going to suceed or bowler
				if batting_prob >= bowling_prob:
					runs = random.choice([0, 2, 4, 6])
					#updating the batting team score
					self.scores[self.batting_team] += runs
					self.batter.runs += runs
					self.overs += 0.1
					time.sleep(1)
					self.commentary()

					#check wheather team is chasing and has already passed the target
					if self.innings == 2 and self.scores[self.batting_team] > self.scores[self.bowling_team]:
						return 2
				else:
					#updating the batting team lost wickets
					self.wickets[self.batting_team] += 1
					self.bowler.wickets += 1
					self.overs += 0.1
					time.sleep(1)
					self.commentary()
					print("wicket Lost !!!")

					#checking wheather all wickets are lost or not...
					if self.wickets[self.batting_team] == 10:
						return 0

					#lost wicket means new player has to come for batting
					self.batter = self.batting_team.next_to_bat()
					self.batter.matches += 1
				
			self.overs = count
		return 0
	def change_innings(self):
		self.teams[0], self.teams[1] = self.teams[1], self.teams[0]
		self.scores = {self.teams[0]:0, self.teams[1]: self.scores[self.batting_team]}
		self.wickets = {self.teams[0]:0, self.teams[1]: 0}
		self.innings = 2
		self.overs = 0


	def start_innings(self):
		print("Match Started in XYZ ground")
		print("First Innings Started: \n")
		time.sleep(1)
		self.simulate_innings()
		time.sleep(1)
		print("---One Innings Done---\n")
		print(f"{self.batting_team.name} scored {self.scores[self.batting_team]}/{self.wickets[self.batting_team]} in {self.overs:.1f}")
		self.change_innings()
		time.sleep(1)
		print("\n---Second Innings--- \n")

		k = self.simulate_innings()
		time.sleep(1)
		print("---Second Innings Done---\n")
		print(f"{self.batting_team.name} scored {self.scores[self.batting_team]}/{self.wickets[self.batting_team]} in {self.overs:.1f}")

		if k == 2:
			time.sleep(2)
			print(f"\n{self.batting_team.name} has succesfully chased the score")
			print(f"Congratulations!! to winning captain: {self.batting_team.captain.name}")
			print(f"Best Batter: {self.best_players(self.batting_team)[0].name} \nBest Bowler: {self.best_players(self.batting_team)[1].name}")
		else:
			time.sleep(2)
			print(f"\nMatch Outcome: {self.bowling_team.name} defended their score")
			print(f"Congratulations!! to winning captain: {self.bowling_team.captain.name}")
			print(f"Best Batter: {self.best_players(self.bowling_team)[0].name} \nBest Bowler: {self.best_players(self.bowling_team)[1].name}")
	
	#determine the best players from the winning side
	def best_players(self, team):
		best_batter = sorted(team.players, key =  lambda x:x.runs, reverse=True)[0]
		best_bowler = sorted(team.players, key = lambda x:x.wickets, reverse = True)[0]

		return [best_batter, best_bowler]

class Match:
	def __init__(self, teams, field):
		self.teams = teams
		self.field = field 
		self.umpire = Umpire(teams, field)

	def start_match(self):
		#to start the match innings
		self.umpire.start_innings()

#deciding the playing eleven
player1 = Player("MS Dhoni", 0.18, 0.3, 0.87, 0.65, 0.9, 34)
player2 = Player("Vi K", 0.8, 0.32, 0.87, 0.65, 0.89, 24)
player3 = Player("Stuart", 0.58, 0.3, 0.87, 0.65, 0.49, 44)
player4 = Player("Root", 0.81, 0.37, 0.87, 0.65, 0.59, 45)
player5 = Player("Stokes", 0.28, 0.3, 0.7, 0.65, 0.9, 26)
player6 = Player("Mint", 0.68, 0.36, 0.8, 0.65, 0.29, 86)
player7 = Player("Vire", 0.48, 0.23, 0.73, 0.65, 0.49, 67)
player8 = Player("Neim", 0.58, 0.38, 0.87, 0.65, 0.99, 37)
player9 = Player("Strine", 0.38, 0.23, 0.77, 0.65, 0.9, 44)
player10 = Player("Decca", 0.51, 0.32, 0.37, 0.65, 0.29, 54)
player11 = Player("Lopez", 0.47, 0.3, 0.87, 0.65, 0.97, 64)


player12 = Player("Wixer", 0.48, 0.37, 0.87, 0.65, 0.9, 34)
player13= Player("Nigel", 0.8, 0.3, 0.27, 0.65, 0.9, 32)
player14= Player("Patern", 0.28, 0.23, 0.17, 0.15, 0.69, 38)
player15 = Player("Usman", 0.28, 0.38, 0.87, 0.85, 0.92, 24)
player16 = Player("Warner", 0.38, 0.68, 0.57, 0.56, 0.98, 34)
player17 = Player("Mistic", 0.54, 0.23, 0.12, 0.68, 0.19, 38)
player18 = Player("Norile", 0.48, 0.3, 0.8, 0.6, 0.9, 30)
player19 = Player("Vibert", 0.8, 0.33, 0.87, 0.5, 0.9, 30)
player20= Player("Nick", 0.28, 0.3, 0.17, 0.65, 0.9, 31)
player21 = Player("Darter", 0.85, 0.3, 0.87, 0.65, 0.9, 32)
player22 = Player("MST", 0.18, 0.3, 0.85, 0.65, 0.9, 34)

#setting the teams up
team1 = Team("RCC", [player1,player2,player3,player4,player5,player6,player7,player8,player9,player10,player11])
team2 = Team("TCC", [player12,player13,player22,player14,player15,player16,player17,player18,player19,player20,player21])

#setting the captain and batting order
team1.set_captain(player2) 
team1.set_batting_order()
team2.set_captain(player12)
team2.set_batting_order()

#Here we provide field details
field = Field("Large",0.6, "Wet", 0.3)
match = Match([team1, team2], field)

#Starting Match
match.start_match()


#we can also determine the stats of each player
#can also use a function to get stats of a specific player by the user..
print("\n---Getting Stats ---")
time.sleep(2)
#get stats of any player
player1.get_stats()
time.sleep(2)
print("\n")
player17.get_stats()