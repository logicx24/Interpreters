from sys import *
import os.path

class BrainFuckException(object):

	def throw(self, message):
		print(message)
		exit()

class Brainfuck(object):

	def __init__(self):
		self.valid_symbols = ['+', '-', '>', '<', '.', ',', '[', ']', '*']
		self.programArray = [0]*30000
		self.counter = 0
		self.code_dict = self.functions()
		self.exceptionObj = BrainFuckException()

	def setCode(self, string):
		self.code = self.filterCode(string)

	def setFileCode(self, filename):
		self.code = self.filterCode(open(filename, 'r').read())

	def expandProgramArray(self):
		self.programArray.extend([0]*100)

	def filterCode(self, code):
		return "".join(char for char in code.replace(" ", "") if char in self.valid_symbols)

	def incrementCounter(self):
		self.counter += 1

	def decrementCounter(self):
		self.counter -= 1

	def incrementDeref(self):
		self.programArray[self.counter] += 1

	def decrementDeref(self):
		self.programArray[self.counter] -= 1

	def syntaxErrors(self):
		stack = []
		stackList = ['[']
		stackHash = {']':'['}
		for i in range(len(self.code)):
			letter = self.code[i]
			if letter in stackList:
				stack.insert(0, letter)
			elif letter in stackHash:
				if len(stack) == 0:
					return True
				elif stack.pop(0) != stackHash[letter]:
					return True
		if len(stack) != 0:
			return True
		return False

	def commaFunc(self):
		print('Please enter a single character below.')
		userInput = input()
		# if len(userInput) > 1:
		# 	self.exceptionObj.throw('Only enter one character to the input.')
		self.programArray[self.counter] = int(userInput)

	def functions(self):
		code_dict = {
			'.' : lambda : print(str(chr(self.programArray[self.counter]))),
			'>' : lambda : self.incrementCounter(),
			'<' : lambda : self.decrementCounter(),
			'+' : lambda : self.incrementDeref(),
			'-' : lambda : self.decrementDeref(),
			',' : lambda : self.commaFunc(),
			'*' : lambda : print(self.programArray[self.counter])
		}
		return code_dict

	def loopIndex(self):
		counterToIndex = {}
		loopNumber = 0
		openToClosing = {}
		closingToOpening = {}
		for index, char in enumerate(self.code):
			if char == "[":
				loopNumber += 1
				counterToIndex[loopNumber] = index
			elif char == "]":
				if loopNumber in counterToIndex:
					openToClosing[counterToIndex[loopNumber]] = index
					closingToOpening[index] = counterToIndex[loopNumber]
				loopNumber -= 1
		return openToClosing, closingToOpening

	def executeCode(self):
		if self.syntaxErrors():
			self.exceptionObj.throw('Syntax Error')

		loopHashForward, loopHashBackward = self.loopIndex()

		i = 0
		while i < len(self.code):
			char = self.code[i]
			if char in self.code_dict:
				self.code_dict[char]()
				i += 1
			elif char == '[':
				if self.programArray[self.counter] == 0:
					i = loopHashForward[i] + 1
				else:
					i += 1
			elif char == ']':
				if self.programArray[self.counter] == 0:
					i += 1
				else:
					i = loopHashBackward[i] + 1
			else:
				i += 1

	def repl(self):
		while True:
			self.setCode(input("> "))
			self.executeCode()


if __name__ == "__main__":
	brainfuck = Brainfuck()
	if len(argv) == 1:
		brainfuck.repl()
	elif len(argv) >= 2:
		if os.path.isfile(argv[1]):
			brainfuck.setFileCode(argv[1])
			brainfuck.executeCode()
		else:
			print("This file does not exist. Check your path.")

