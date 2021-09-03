import sys
import os
import time
import random
from collections import Counter
import pygame
from pygame import mixer

pygame.init()
mixer.init()

screen_width = 800
screen_height = 600
first_table_dice_x_position = 100;
screen = pygame.display.set_mode((screen_width, screen_height))
smallfont = pygame.font.SysFont('Corbel',20)
xsmallfont = pygame.font.SysFont('Corbel',16)
xsmallfontbold = pygame.font.SysFont('Corbel',16, bold=True)
clock = pygame.time.Clock()
game_over = False
white = (255,255,255)
green = (0,102,0)
black = (0,0,0)
red = (255,0,0)
ai = False

script_dir = os.path.dirname(os.path.realpath(__file__))

#Dice images
dice_1 = pygame.image.load(os.path.join(script_dir, 'assets/images/1.png'))
dice_2 = pygame.image.load(os.path.join(script_dir, 'assets/images/2.png'))
dice_3 = pygame.image.load(os.path.join(script_dir, 'assets/images/3.png'))
dice_4 = pygame.image.load(os.path.join(script_dir, 'assets/images/4.png'))
dice_5 = pygame.image.load(os.path.join(script_dir, 'assets/images/5.png'))
dice_6 = pygame.image.load(os.path.join(script_dir, 'assets/images/6.png'))
bg_image = pygame.image.load(os.path.join(script_dir, 'assets/images/felt_800x600.png'))

#Dice Audio
dice_roll_sound = pygame.mixer.Sound(os.path.join(script_dir, 'assets/audio/roll.mp3'))
dice_take_sound = pygame.mixer.Sound(os.path.join(script_dir, 'assets/audio/take.mp3'))
select_score_sound = pygame.mixer.Sound(os.path.join(script_dir, 'assets/audio/select.mp3'))
channel = pygame.mixer.Channel(0)
channel.set_volume(0.2)
# pygame.mixer.music.load(os.path.join(script_dir, 'assets/audio/bg.mp3'))
# pygame.mixer.music.play()

class Dice():
	DiceOnTable = {'d1': 7, 'd2': 7, 'd3': 7, 'd4': 7, 'd5': 7}
	PersonalDice = {'d1': 0, 'd2': 0, 'd3': 0, 'd4': 0, 'd5': 0}
	AllDice = {}
	DiceRoll = 0
	Score = {
		'ones' : 0,
		'twos' : 0,
		'threes' : 0,
		'fours' : 0,
		'fives' : 0,
		'sixes' : 0,
		'threeofakind' : 0,
		'fourofakind' : 0,
		'fullhouse' : 0,
		'smallstraight' : 0,
		'largestraight' : 0,
		'chance' : 0,
		'yahtzee' : 0
	}
	SetScore = {
		'ones' : 'a',
		'twos' : 'a',
		'threes' : 'a',
		'fours' : 'a',
		'fives' : 'a',
		'sixes' : 'a',
		'topsum': 'a',
		'topbonus' : 'a',
		'threeofakind' : 'a',
		'fourofakind' : 'a',
		'fullhouse' : 'a',
		'smallstraight' : 'a',
		'largestraight' : 'a',
		'chance' : 'a',
		'yahtzee' : 'a'
	}

	def DiceToImages(self, num):
		dice = {
			'1' : dice_1,
			'2' : dice_2,
			'3' : dice_3,
			'4' : dice_4,
			'5' : dice_5,
			'6' : dice_6
		}

		return dice[str(num)]

	def __inti__(self):
		pass

	def RollDice(self):
		self.Score = {
			'ones' : 0,
			'twos' : 0,
			'threes' : 0,
			'fours' : 0,
			'fives' : 0,
			'sixes' : 0,
			'threeofakind' : 0,
			'fourofakind' : 0,
			'fullhouse' : 0,
			'smallstraight' : 0,
			'largestraight' : 0,
			'chance' : 0,
			'yahtzee' : 0
		}

		self.DiceRoll = self.DiceRoll + 1
		# print(self.DiceRoll)
		if self.DiceRoll < 4:
			for k in self.DiceOnTable:
				if self.DiceOnTable[k] != 0:
					dice = random.randint(1, 6)
					self.DiceOnTable[k] = dice
			channel.play(dice_roll_sound)
		self.MergeDice()

	def SetTableDice(self):
		for i, dice in enumerate(self.DiceOnTable.values()):
			if dice == 0 or dice == 7:
				color = green
				label_color = green
			else:
				color = white
				label_color = black
			if i == 0:
				if dice != 0 and dice != 7:
					dice_image = self.DiceToImages(dice)
					screen.blit(dice_image, (first_table_dice_x_position, 258, 60, 60))
			else:
				if dice != 0 and dice != 7:
					dice_image = self.DiceToImages(dice)
					screen.blit(dice_image, (first_table_dice_x_position + (i * 70),258, 60, 60))

	def SetPersonalDice(self):
		for i, dice in enumerate(self.PersonalDice.values()):
			if dice == 0:
				color = green
				label_color = green
			else:
				color = white
				label_color = black
			if i == 0:
				if dice == 0 or dice == 7:
					pass
				else:
					dice_image = self.DiceToImages(dice)
					screen.blit(dice_image, (first_table_dice_x_position,500, 60, 60))
			else:
				if dice == 0 or dice == 7:
					pass
				else:
					dice_image = self.DiceToImages(dice)
					screen.blit(dice_image, (first_table_dice_x_position + (i * 70),500, 60, 60))

	def KeepDice(self, dice_position):
		channel.play(dice_take_sound)
		self.PersonalDice[dice_position] = self.DiceOnTable[dice_position]
		self.DiceOnTable[dice_position] = 0

	def SendDiceBack(self, dice_position):
		channel.play(dice_take_sound)
		self.DiceOnTable[dice_position] = self.PersonalDice[dice_position]
		self.PersonalDice[dice_position] = 0

	def CheckDice(self):
		for v in range(7):
			self.CheckForTop(v)
		
		self.CheckForChance()
		self.CheckForMultiples()
		self.CheckForLargeStraight()
		self.CheckForSmallStraight()

	def CheckForTop(self, num):
		NumOf = []
		for v in self.AllDice:
			if str(self.AllDice[v]) == str(num):
				NumOf.append(1)
		HowMany = str(len(NumOf))

		if num == 1:
			self.Score['ones'] = int(HowMany) * 1

		if num == 2:
			self.Score['twos'] = int(HowMany) * 2

		if num == 3:
			self.Score['threes'] = int(HowMany) * 3

		if num == 4:
			self.Score['fours'] = int(HowMany) * 4

		if num == 5:
			self.Score['fives'] = int(HowMany) * 5

		if num == 6:
			self.Score['sixes'] = int(HowMany) * 6
		

	def CheckForMultiples(self):
		counts = Counter(self.AllDice.values())
		TwoOfAKind = False
		ThreeOfAKind = False

		for v in counts:
			if counts[v] == 5:
				self.Score['yahtzee'] = 50
			if counts[v] == 4:
				self.Score['fourofakind'] = sum(self.AllDice.values())
				self.Score['threeofakind'] = sum(self.AllDice.values())
			if counts[v] == 2:
				pass
				TwoOfAKind = True
			if counts[v] == 3:
				ThreeOfAKind = True
				self.Score['threeofakind'] = sum(self.AllDice.values())

		if TwoOfAKind and ThreeOfAKind:
			self.Score['fullhouse'] = 25

	def CheckForThreeOfAKind(self):
		pass


	def CheckForLargeStraight(self):
		#the below could be done better - needs refactoring
		# self.DiceOnTable = {k: v for k, v in sorted(self.DiceOnTable.items(), key=lambda item: item[1])}

		if ((1 in self.AllDice.values() and
				2 in self.AllDice.values() and
				3 in self.AllDice.values() and
				4 in self.AllDice.values() and
				5 in self.AllDice.values()) or
				(2 in self.AllDice.values() and
				3 in self.AllDice.values() and
				4 in self.AllDice.values() and
				5 in self.AllDice.values() and
				6 in self.AllDice.values())):
			self.Score['largestraight'] = 40


	def CheckForSmallStraight(self):
		#the below could be done better - needs refactoring
		# self.DiceOnTable = {k: v for k, v in sorted(self.DiceOnTable.items(), key=lambda item: item[1]))

		if ((1 in self.AllDice.values() and
				2 in self.AllDice.values() and
				3 in self.AllDice.values() and
				4 in self.AllDice.values()) or
				(2 in self.AllDice.values() and
				3 in self.AllDice.values() and
				4 in self.AllDice.values() and
				5 in self.AllDice.values()) or
				(3 in self.AllDice.values() and
				4 in self.AllDice.values() and
				5 in self.AllDice.values() and
				6 in self.AllDice.values())):
			self.Score['smallstraight'] = 35

	def CheckForChance(self):
		total = 0

		for v in self.AllDice:
			total += self.AllDice[v]

		self.Score['chance'] = total

	def BuildScoreboard(self):
		for i in range(17):
			if i == 0:
				pygame.draw.rect(screen,black,[532,50,246,1])
			elif i == 7:
				pygame.draw.rect(screen,black,[532,260,246,2])
			elif i == 9:
				pygame.draw.rect(screen,black,[532,320,246,2])
			elif i == 16:
				pygame.draw.rect(screen,black,[532,530,246,2])
			else:
				pygame.draw.rect(screen,black,[532,50 + (i * 30),246,1])

		pygame.draw.rect(screen,black,[680,50,1,510])
		pygame.draw.rect(screen,black,[730,50,1,510])

		player_1 = xsmallfont.render('YOU',True,black)
		screen.blit(player_1, (689,60))	

		ones = xsmallfont.render('Ones',True,black)
		screen.blit(ones, (535,90))	

		twos = xsmallfont.render('Twos',True,black)
		screen.blit(twos, (535,120))	

		threes = xsmallfont.render('Threes',True,black)
		screen.blit(threes, (535,150))	

		fours = xsmallfont.render('Fours',True,black)
		screen.blit(fours, (535,180))	

		fives = xsmallfont.render('Fives',True,black)
		screen.blit(fives, (535,210))	

		sixes = xsmallfont.render('Sixes',True,black)
		screen.blit(sixes, (535,240))	

		sunbtotal = xsmallfont.render('Sum',True,black)
		screen.blit(sunbtotal, (535,270))	

		bonus = xsmallfont.render('Bonus',True,black)
		screen.blit(bonus, (535,300))	

		threeofakind = xsmallfont.render('Three of a kind',True,black)
		screen.blit(threeofakind, (535,330))	

		fourfofakind = xsmallfont.render('Four of a kind',True,black)
		screen.blit(fourfofakind, (535,360))	

		fullhouse = xsmallfont.render('Full house',True,black)
		screen.blit(fullhouse, (535,390))	

		smallstraight = xsmallfont.render('Small straight',True,black)
		screen.blit(smallstraight, (535,420))	

		largestraight = xsmallfont.render('Large straight',True,black)
		screen.blit(largestraight, (535,450))	

		chance = xsmallfont.render('Chance',True,black)
		screen.blit(chance, (535,480))	

		yahtzee = xsmallfont.render('Yahtzee',True,black)
		screen.blit(yahtzee, (535,510))	

		total = xsmallfont.render('Total',True,black)
		screen.blit(total, (535,540))

	def DisplayScore(self):
		x_position = 700

		ones = self.DisplayScoreNumberColors(self.Score['ones'], 'ones')
		screen.blit(ones, (x_position,90))	

		twos = self.DisplayScoreNumberColors(self.Score['twos'], 'twos')
		screen.blit(twos, (x_position,120))	

		threes = self.DisplayScoreNumberColors(self.Score['threes'], 'threes')
		screen.blit(threes, (x_position,150))	

		fours = self.DisplayScoreNumberColors(self.Score['fours'], 'fours')
		screen.blit(fours, (x_position,180))	

		fives = self.DisplayScoreNumberColors(self.Score['fives'], 'fives')
		screen.blit(fives, (x_position,210))	

		sixes = self.DisplayScoreNumberColors(self.Score['sixes'], 'sixes')
		screen.blit(sixes, (x_position,240))		

		threeofakind = self.DisplayScoreNumberColors(self.Score['threeofakind'], 'threeofakind')
		screen.blit(threeofakind, (x_position,330))	

		fourfofakind = self.DisplayScoreNumberColors(self.Score['fourofakind'], 'fourofakind')
		screen.blit(fourfofakind, (x_position,360))	

		fullhouse = self.DisplayScoreNumberColors(self.Score['fullhouse'], 'fullhouse')
		screen.blit(fullhouse, (x_position,390))	

		smallstraight = self.DisplayScoreNumberColors(self.Score['smallstraight'], 'smallstraight')
		screen.blit(smallstraight, (x_position,420))	

		largestraight = self.DisplayScoreNumberColors(self.Score['largestraight'], 'largestraight')
		screen.blit(largestraight, (x_position,450))	

		chance = self.DisplayScoreNumberColors(self.Score['chance'], 'chance')
		screen.blit(chance, (x_position,480))	

		yahtzee = self.DisplayScoreNumberColors(self.Score['yahtzee'], 'yahtzee')
		screen.blit(yahtzee, (x_position,510))	

		total = xsmallfont.render('0',True,black)
		screen.blit(total, (x_position,540))

	def DisplayScoreNumberColors(self, num, type):
		if self.SetScore[type] == 'a':
			if num != 'a':
				return xsmallfont.render(str(num),True,red)
			else:
				return xsmallfont.render(str(num),True,black)
		else:
			return xsmallfontbold.render(str(self.SetScore[type]),True,black)

	def MergeDice(self):
		#Remove none values - or dice taken away
		DiceOnTable = {k: v for k, v in self.DiceOnTable.items() if v is not 0}
		PersonalDice = {k: v for k, v in self.PersonalDice.items() if v is not 0}
		self.AllDice = res = {**DiceOnTable, **PersonalDice}

	def SetInlineScore(self,set):
		if self.DiceRoll != 0 and self.SetScore[set] == 'a':
			channel.play(select_score_sound)
			self.SetScore[set] = self.Score[set]
			self.ResetDice()

	def ResetDice(self):
		self.DiceOnTable = {'d1': 7, 'd2': 7, 'd3': 7, 'd4': 7, 'd5': 7}
		self.PersonalDice = {'d1': 0, 'd2': 0, 'd3': 0, 'd4': 0, 'd5': 0}
		self.Score = {
			'ones' : 0,
			'twos' : 0,
			'threes' : 0,
			'fours' : 0,
			'fives' : 0,
			'sixes' : 0,
			'threeofakind' : 0,
			'fourofakind' : 0,
			'fullhouse' : 0,
			'smallstraight' : 0,
			'largestraight' : 0,
			'chance' : 0,
			'yahtzee' : 0
		}
		self.DiceRoll = 0

	def TopSumAnBonus(self):
		x_position = 700

		if (
			self.SetScore['ones'] != 'a' and
			self.SetScore['twos'] != 'a' and
			self.SetScore['threes'] != 'a' and
			self.SetScore['fours'] != 'a' and
			self.SetScore['fives'] != 'a' and
			self.SetScore['sixes'] != 'a' 
			):
			top_total = int(self.SetScore['ones']) + int(self.SetScore['twos']) + int(self.SetScore['threes']) + int(self.SetScore['fours']) + int(self.SetScore['fives']) + int(self.SetScore['sixes'])

			subtotal = xsmallfont.render(str(top_total),True,black)
			screen.blit(subtotal, (x_position,270))

			self.SetScore['topsum'] = top_total

			if top_total >= 63:
				self.SetScore['topbonus'] = 35
				bonus = xsmallfont.render('35',True,black)
				screen.blit(bonus, (x_position,300))	
			else:
				self.SetScore['topbonus'] = 0
				bonus = xsmallfont.render('0',True,black)
				screen.blit(bonus, (x_position,300))
		else:
			subtotal = xsmallfont.render('0',True,black)
			screen.blit(subtotal, (x_position,270))	

	def FinalScore(self):
		final = False
		total = 0

		if ('a' in self.SetScore.values()):
			pass
		else:
			final = True
			for dice_label, dice in self.SetScore.items():
				if dice_label != 'topsum':
					total += dice
			text1 = smallfont.render('Game Over',True,black)
			text2 = smallfont.render('Your Score: ' + str(total),True,black)
			text3 = smallfont.render('Exit - New Game',True,black)
			pygame.draw.rect(screen,(255,255,255),[120,150,300,150])
			screen.blit(text1, (215,160))
			screen.blit(text2, (215,200))
			screen.blit(text3, (215,240))


dice = Dice()

class PlayerOne(Dice):
	P1Dice = {'d1': 0, 'd2': 0, 'd3': 0, 'd4': 0, 'd5': 0}
	P1AllDice = {}
	P1DiceRoll = 0
	P1SetScore = {
		'ones' : 'a',
		'twos' : 'a',
		'threes' : 'a',
		'fours' : 'a',
		'fives' : 'a',
		'sixes' : 'a',
		'threeofakind' : 'a',
		'fourofakind' : 'a',
		'fullhouse' : 'a',
		'smallstraight' : 'a',
		'largestraight' : 'a',
		'chance' : 'a',
		'yahtzee' : 'a'
	}

class AI(Dice):
	AIDice = {'d1': 0, 'd2': 0, 'd3': 0, 'd4': 0, 'd5': 0}
	AIAllDice = {}
	AIDiceRoll = 0
	AISetScore = {
		'ones' : 'a',
		'twos' : 'a',
		'threes' : 'a',
		'fours' : 'a',
		'fives' : 'a',
		'sixes' : 'a',
		'threeofakind' : 'a',
		'fourofakind' : 'a',
		'fullhouse' : 'a',
		'smallstraight' : 'a',
		'largestraight' : 'a',
		'chance' : 'a',
		'yahtzee' : 'a'
	}


def GameLoop():
	while not game_over:
		screen.blit(bg_image, (0, 0))
		pygame.draw.rect(screen,(255,255,255),[530,20,250,550])
		text = smallfont.render('Roll Dice',True,(255,255,255))
		pygame.draw.rect(screen,(0,0,0),[200,450,140,40])
		screen.blit(text, (240,460))
		mouse = pygame.mouse.get_pos()

		for event in pygame.event.get():
			# print(event)
			if event.type == pygame.QUIT:
				sys.exit()

			elif event.type == pygame.MOUSEBUTTONDOWN:
	              
				if 200 <= mouse[0] <= 200+140 and 450 <= mouse[1] <= 450+40:					
					dice.RollDice()
					dice.CheckDice()
				#Top Dice
				elif 105 <= mouse[0] <= 154 and 259 <= mouse[1] <= 311:
					dice.KeepDice('d1')
					
				elif 171 <= mouse[0] <= 223 and 259 <= mouse[1] <= 311:
					dice.KeepDice('d2')
					
				elif 239 <= mouse[0] <= 290 and 259 <= mouse[1] <= 311:
					dice.KeepDice('d3')

				elif 313 <= mouse[0] <= 364 and 259 <= mouse[1] <= 311:
					dice.KeepDice('d4')

				elif 382 <= mouse[0] <= 434 and 259 <= mouse[1] <= 311:
					dice.KeepDice('d5')
				#Bottom Dice
				elif 106 <= mouse[0] <= 153 and 500 <= mouse[1] <= 540:
					dice.SendDiceBack('d1')
					
				elif 169 <= mouse[0] <= 222 and 500 <= mouse[1] <= 540:
					dice.SendDiceBack('d2')
					
				elif 240 <= mouse[0] <= 296 and 500 <= mouse[1] <= 540:
					dice.SendDiceBack('d3')

				elif 311 <= mouse[0] <= 367 and 500 <= mouse[1] <= 540:
					dice.SendDiceBack('d4')

				elif 380 <= mouse[0] <= 435 and 500 <= mouse[1] <= 540:
					dice.SendDiceBack('d5')

				elif 682 <= mouse[0] <= 729 and 82 <= mouse[1] <= 106:
					dice.SetInlineScore('ones')

				elif 682 <= mouse[0] <= 729 and 113 <= mouse[1] <= 136:
					dice.SetInlineScore('twos')

				elif 682 <= mouse[0] <= 729 and 142 <= mouse[1] <= 168:
					dice.SetInlineScore('threes')

				elif 682 <= mouse[0] <= 729 and 174 <= mouse[1] <= 198:
					dice.SetInlineScore('fours')

				elif 682 <= mouse[0] <= 729 and 202 <= mouse[1] <= 227:
					dice.SetInlineScore('fives')

				elif 682 <= mouse[0] <= 729 and 234 <= mouse[1] <= 258:
					dice.SetInlineScore('sixes')

				elif 682 <= mouse[0] <= 729 and 327 <= mouse[1] <= 347:
					dice.SetInlineScore('threeofakind')

				elif 682 <= mouse[0] <= 729 and 352 <= mouse[1] <= 376:
					dice.SetInlineScore('fourofakind')

				elif 682 <= mouse[0] <= 729 and 380 <= mouse[1] <= 407:
					dice.SetInlineScore('fullhouse')

				elif 682 <= mouse[0] <= 729 and 413 <= mouse[1] <= 436:
					dice.SetInlineScore('smallstraight')

				elif 682 <= mouse[0] <= 729 and 443 <= mouse[1] <= 464:
					dice.SetInlineScore('largestraight')

				elif 682 <= mouse[0] <= 729 and 474 <= mouse[1] <= 498:
					dice.SetInlineScore('chance')

				elif 682 <= mouse[0] <= 729 and 504 <= mouse[1] <= 526:
					dice.SetInlineScore('yahtzee')

				elif 216 <= mouse[0] <= 243 and 242 <= mouse[1] <= 254:
					sys.exit()

			elif event.type == pygame.KEYDOWN:

				if event.key == pygame.K_ESCAPE:
					sys.exit()


		clock.tick(30)
		dice.SetTableDice()
		dice.SetPersonalDice()
		dice.BuildScoreboard()
		dice.DisplayScore()
		dice.TopSumAnBonus()
		dice.FinalScore()
		pygame.display.flip()

GameLoop()

pygame.quit()
quit()