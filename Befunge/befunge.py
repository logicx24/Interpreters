#https://www.reddit.com/r/dailyprogrammer/comments/270mll/612014_challenge_164_hard_what_the_funge_is_this/
import sys, random

class Befunge:

	def __init__(self, filename):

		self.stack = []
		self.curr = [0,0]
		self.currDir = [1,0]
		self.stringMode = False

		with open(filename) as f:
			txt = f.read().strip().split("\n")
			self.input = txt[0].split()
			txt = "\n".join(txt[1:])
			self.code = [list(line) for line in txt.strip().split("\n")]
			maxline = max(len(cod) for cod in self.code)
			self.code = [line + list((maxline - len(line))*" ") for line in self.code]

		self.dims = [len(self.code), len(self.code[0])]

		self.instrSet = {
			">": lambda: self.setdir(1, 0),
			"<": lambda: self.setdir(-1, 0),
			"^": lambda: self.setdir(0, -1),
			"v": lambda: self.setdir(0, 1),
			"+": lambda: self.push(self.pop()+self.pop()),
			"-": lambda: self.push(-self.pop()+self.pop()),
			"*": lambda: self.push(self.pop()*self.pop()),
			"/": lambda: self.push(int(1.0/self.pop() * self.pop())),
			":": lambda: self.stack.extend([self.pop()] * 2),
			"!": lambda: self.push(1 if self.pop == 0 else 0),
			"`": lambda: self.push(1 if self.pop() < self.pop() else 0),
			"?": lambda: self.setdir(*random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])),
			"_": lambda: self.setdir(*((1,0) if self.pop() == 0 else (-1,0))),
			"|": lambda: self.setdir(*((0,1) if self.pop() == 0 else (0,-1))),
			"$": lambda: self.pop(),
			".": lambda: sys.stdout.write(str(self.pop())),
			",": lambda: sys.stdout.write(chr(self.pop())),
			"p": lambda: self.p(),
			"g": lambda: self.g(),
			"&": lambda: self.push(int(self.input.pop())),
			"~": lambda: self.push(ord(self.input(pop()))),
			"\\": lambda: self.swap()
		}

	def swap(self):
		t1, t2 = self.pop(), self.pop()
		self.push(t1)
		self.push(t2)

	def setStringMode(self):
		self.stringMode = not self.stringMode

	def setdir(self, x, y):
		self.currDir = [x, y]

	def push(self, val):
		self.stack.append(val)

	def pop(self):
		return 0 if not self.stack else self.stack.pop()

	def p(self):
		y = self.pop()
		x = self.pop()
		self.code[x][y] = self.pop()

	def g(self):
		y, x = self.pop(), self.pop()
		if x >= self.dims[1] or y >= self.dims[0]:
			self.push(0)
		else:
			self.push(self.code[y][x])

	def updatePointer(self):
		self.curr[0] = (self.curr[0] + self.currDir[0]) % self.dims[1]
		self.curr[1] = (self.curr[1] + self.currDir[1]) % self.dims[0]

	def eventLoop(self):
		
		while self.code[self.curr[1]][self.curr[0]] != "@":
			currChar = self.code[self.curr[1]][self.curr[0]]
			# print("------------------------------")
			# print(currChar)
			# print(self.stack)
			# print(self.currDir)
			# print(self.curr)
			# print(self.stringMode)
			# print("-------------------------------")
			if currChar == '"':
				self.setStringMode()
			elif self.stringMode:
				self.push(ord(currChar))
			elif currChar == " ":
				pass
			elif currChar in "1234567890":
				self.push(int(currChar))
			elif currChar == "#":
				self.updatePointer()
			elif currChar == "%":
				x, y = self.pop(), self.pop()
				self.push(y%x)
			else:
				self.instrSet[currChar]()
			self.updatePointer()




	
