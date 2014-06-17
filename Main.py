#!env python

import random

MIN_WORD_LENGTH = 3
MAX_WORD_LENGTH = 7
SCORE_MULTIPLIER = 25

class Wordlist(object):
	def __init__(self, file):
		self.words = [[] for x in range(MAX_WORD_LENGTH + 1)] # Add 1 because I want to store 7-letter words at index 7, not index 6
		toRead = open(file, 'r')
		for line in toRead:
			word = line[0:-1] # Strip \n off
			i = len(word)
			if i >= MIN_WORD_LENGTH and i <= MAX_WORD_LENGTH:
				self.words[len(word)].append(word)

	def getRandom(self, length):
		return random.choice(self.words[length])

	def isValid(self, word):
		return word in self.words[len(word)]

class Game(object):
	def __init__(self, wordList):
		self.wordList = wordList
		self.newGame()

	def newGame(self):
		self.currentWord = self.wordList.getRandom(7)
		self.guesses = []
		self.totalScore = 0
		self.rounds = [
			# word length, offset
			(3, 0),
			(4, 0),
			(4, 1),
			(4, 2),
			(4, 3),
			(5, 2),
			(5, 1),
			(5, 0),
			(6, 0),
			(6, 1),
			(7, 0),
		];
		# print self.currentWord

	def guess(self, word):
		length = self.rounds[0][0]
		if (len(word)) != length:
			self.scoreboard()
			print "Words must be " + str(length) + " letters"
			return True
		if not self.wordList.isValid(word):
			self.scoreboard()
			print word + " is not a valid word"
			return True
		
		score = 0

		# Copy the secret and guessed words into lists so we can cross off letters as they're scored
		placeholderGame = list(self.currentWord)
		placeholderPlayer = list(word.lower())

		# Check if any characters are exactly correct
		for i in range(length):
			# Need to account for the fact that the guessed word is offset relative to the secret word
			offsetIndex = i + self.rounds[0][1]
			if word[i] == placeholderGame[offsetIndex]:
				score += 4 * SCORE_MULTIPLIER
				placeholderGame[offsetIndex] = "_"
				placeholderPlayer[i] = "_"

		# Check if any characters are correct, but in wrong spots
		for i in range(length):
			if placeholderPlayer[i] == "_":
				continue
			if placeholderPlayer[i] in placeholderGame:
				j = placeholderGame.index(placeholderPlayer[i])
				score += 1 * SCORE_MULTIPLIER
				placeholderGame[j] = "_"

		# Build a string to repesent the guess on the scoreboard
		guess = "." * self.rounds[0][1] + word
		while len(guess) < MAX_WORD_LENGTH:
			guess = guess + "."
		guess = guess + " "

		self.guesses.append((guess, score))
		self.totalScore = self.totalScore + score

		self.rounds.pop(0)

		if len(self.rounds) > 0:
			self.scoreboard()
			return True
		else:
			self.gameOver()
			return False

	def scoreboard(self):
		print "\n" * 100
		for guess in self.guesses:
			print guess[0] + str(guess[1])

		if len(self.rounds) > 0:
			current = " " * self.rounds[0][1] + "_" * self.rounds[0][0] + "\n\n(" + str(self.rounds[0][0]) + " letters)"
			print current

	def gameOver(self):
		self.scoreboard();
		print
		print "The secret word was \"" + self.currentWord + "\""
		print "Final score: " + str(self.totalScore)
		print

wordList = Wordlist('words.txt')
game = Game(wordList)

# for i in [3] + [4] * 4 + [5] * 3 + [6] * 2 + [7]:
	# game.guess(wordList.getRandom(i))

game.scoreboard()
while(game.guess(raw_input())):
	pass