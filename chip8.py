import sys
from random import randint, seed
from time import time

class Chip8:

	def __init__(self):
		self.fontset = 	[0xF0, 0x90, 0x90, 0x90, 0xF0, 
	  	0x20, 0x60, 0x20, 0x20, 0x70, 
	  	0xF0, 0x10, 0xF0, 0x80, 0xF0, 
		0xF0, 0x10, 0xF0, 0x10, 0xF0, 
	 	0x90, 0x90, 0xF0, 0x10, 0x10, 
		0xF0, 0x80, 0xF0, 0x10, 0xF0, 
	    	0xF0, 0x80, 0xF0, 0x90, 0xF0, 
	    	0xF0, 0x10, 0x20, 0x40, 0x40, 
	    	0xF0, 0x90, 0xF0, 0x90, 0xF0, 
		0xF0, 0x90, 0xF0, 0x10, 0xF0, 
		0xF0, 0x90, 0xF0, 0x90, 0x90, 
		0xE0, 0x90, 0xE0, 0x90, 0xE0, 
	 	0xF0, 0x80, 0x80, 0x80, 0xF0, 
	    	0xE0, 0x90, 0x90, 0x90, 0xE0, 
	    	0xF0, 0x80, 0xF0, 0x80, 0xF0, 
	 	0xF0, 0x80, 0xF0, 0x80, 0x80]

	def initialize(self, pixels):
		seed()
		self.stack = []
		self.opcode = 0
		self.memory = [0] * 4096
		self.pc = 0x200
		self.I = 0
		self.sp = 0
		self.V = [0] * 16
		self.keys = [0] * 16
		#Init clear screen
		self.graphics = [0] * pixels

		#Python timer
		self.t_last = time()

		#Fontset
		for i in range(80):
			self.memory[i] = self.fontset[i]
		
		self.delay_timer = 0
		self.sound_timer = 0		

		self.draw_flag = True

	def load_game(self, file_name):
		with open(file_name, "rb") as f:
			byte = f.read()
			for i in range(len(byte)):
				self.memory[self.pc + i] = byte[i]

	def emulate_cycle(self):
		#Gets opcode
		self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]
		
		#Uncomment for opcode debugging
		#print(hex(self.opcode))
		#print(hex(self.pc))

		#Decodes opcode
		vx = (self.opcode & 0x0F00) >> 8
		vy = (self.opcode & 0x00F0) >> 4


		#0---
		if(self.opcode & 0xF000 == 0x0000):
			#OOEO
			if(self.opcode == 0x00E0):
				for i in range(len(self.graphics)):
					self.graphics[i] = 0
				self.draw_flag = True

			#OOEE
			elif(self.opcode == 0x00EE):
				self.pc = self.stack.pop()	
		
			#0NNN
			elif(self.opcode & 0x0F00 != 0x0000):
				self.pc = (self.opcode & 0x0FFF) - 2
				
			#Not found:
			else:
				self.pc -= 2
		#1NNN
		elif(self.opcode & 0xF000 == 0x1000):
			self.pc = (self.opcode & 0x0FFF) - 2

		#2NNN
		elif(self.opcode & 0xF000 == 0x2000):
			self.stack.append(self.pc)
			self.pc = (self.opcode & 0x0FFF) - 2

		#3XNN
		elif(self.opcode & 0xF000 == 0x3000):
			if self.V[vx] == self.opcode & 0x00FF:
				self.pc += 2
		
		#4XNN
		elif(self.opcode & 0xF000 == 0x4000):
			if self.V[vx] != self.opcode & 0x00FF:
				self.pc += 2

		#5XY0
		elif(self.opcode & 0xF000 == 0x5000):
			if self.V[vx] == self.V[vy]:
				self.pc += 2			

		#6XNN
		elif(self.opcode & 0xF000 == 0x6000):
			self.V[vx] = self.opcode & 0x00FF
		
		#7XNN
		elif(self.opcode & 0xF000 == 0x7000):
			self.V[vx] += self.opcode & 0x00FF
			self.V[vx] &= 0xFF

		#8---
		elif(self.opcode & 0xF000 == 0x8000):
			l = self.opcode & 0x000F
			#8XY0
			if(l == 0x0000):
				self.V[vx] = self.V[vy]
			#8XY1
			elif(l == 0x0001):
				self.V[vx] = self.V[vx] | self.V[vy]
			#8XY2
			elif(l == 0x0002):
				self.V[vx] = self.V[vx] & self.V[vy]				

			#8XY3
			elif(l == 0x0003):
				self.V[vx] = self.V[vx] ^ self.V[vy]			

			#8XY4
			elif(l == 0x0004):
				self.V[vx] += self.V[vy]
				if self.V[vx] > 0xFF:
					self.V[0xF] = 1
				else:
					self.V[0xF] = 0
				self.V[vx] &= 0xFF

			#8XY5
			elif(l == 0x0005):
				if self.V[vx] < self.V[vy]:
					self.V[0xF] = 0
				else:
					self.V[0xF] = 1
				self.V[vx] -= self.V[vy]
				self.V[vx] &= 0xFF

			#8XY6
			elif(l == 0x0006):
				self.V[0xF] = self.V[vx] & 0x01
				self.V[vx] = self.V[vx] >> 1

			#8XY7
			elif(l == 0x0007):
				if self.V[vx] > self.V[vy]:
					self.V[0xF] = 0
				else:
					self.V[0xF] = 1
				self.V[vx] = self.V[vy] - self.V[vx]
				self.V[vx] &= 0xFF

			#8XYE
			elif(l == 0x000E):
				self.V[0xF] = self.V[vx] & 0x80
				self.V[vx] = self.V[vx] << 1

			else:
				#Not found
				self.pc -= 2

		#9XY0
		elif(self.opcode & 0xF000 == 0x9000):
			if self.V[vx] != self.V[vy]:
				self.pc += 2

		#ANNN
		elif(self.opcode & 0xF000 == 0xA000):
			self.I = self.opcode & 0x0FFF
	
		#BNNN
		elif(self.opcode & 0xF000 == 0xB000):
			self.pc = (self.opcode & 0x0FFF) + self.V[0x0] - 2
	
		#CXNN
		elif(self.opcode & 0xF000 == 0xC000):
			rand_int = randint(0, 0xFF)
			self.V[vx] = rand_int & (self.opcode & 0x00FF)

		#DXYN
		elif(self.opcode & 0xF000 == 0xD000):
			xcord = self.V[vx] 
			ycord = self.V[vy]
			height = self.opcode & 0x000F
			pixel = 0
			self.V[0xF] = 0

			for y in range(height):
				pixel = self.memory[self.I + y]
				for x in range(8):
					i = xcord + x + ((y + ycord) * 64)
					if pixel & (0x80 >> x) != 0 and not (y + ycord  >= 32 or x + xcord >= 64):
						if self.graphics[i] == 1:
							self.V[0xF] = 1
						self.graphics[i] ^= 1

			self.draw_flag = True

		#E---
		elif(self.opcode & 0xF000 == 0xE000):
			#EX9E
			if (self.opcode & 0x00FF == 0x009E):
				if self.keys[self.V[vx]] == 1:
					self.pc += 2

			#EXA1
			elif (self.opcode & 0x00FF == 0x00A1):
				if self.keys[self.V[vx]] == 0:
					self.pc += 2

			#Not found
			else:
				self.pc -= 2
			

		#F---
		elif(self.opcode & 0xF000 == 0xF000):
			nn = self.opcode & 0x00FF

			#FX07
			if(nn == 0x0007):
				self.V[vx] = self.delay_timer

			#FX0A
			elif(nn == 0x000A):
				key = -1
				for i in range(len(self.keys)):
					if self.keys[i] == 1:
						key = i
						break
				if key >= 0:
					self.V[vx] = key	
				else:		
					self.pc -= 2
			#FX15
			elif(nn == 0x0015):
				self.delay_timer = self.V[vx]

			#FX18
			elif(nn == 0x0018):
				self.sound_timer = self.V[vx]			
			
			#FX1E
			elif(nn == 0x001E):
				self.I += self.V[vx]			

			#FX29
			elif(nn == 0x0029):
				self.I = self.V[vx] * 5			

			#FX33
			elif(nn == 0x0033):
				self.memory[self.I] = self.V[vx] // 100
				self.memory[self.I + 1] = (self.V[vx] // 10) % 10
				self.memory[self.I + 2] = (self.V[vx] % 100) % 10
	
			#FX55	
			elif(nn == 0x0055):
				for n in range(vx + 1):
					self.memory[self.I + n] = self.V[n]			

			#FX65
			elif(nn == 0x0065):
				for n in range(vx + 1):
					self.V[n] = self.memory[self.I + n]			

			#Not found
			else:
				self.pc -= 2


	
		#Not currently made print
		else:
			print(hex(self.opcode))
			#saves for debuging purposes
			self.pc -= 2

		self.pc += 2

		pytime = time()	
		if pytime - self.t_last >= 1.0/60:
			if self.delay_timer > 0:
				self.delay_timer -= 1
	
			if self.sound_timer > 0:
				sys.stdout.write("\a") 
				self.sound_timer -= 1
			
			self.t_last = pytime


if __name__ == "__main__":
	from main import main_func
	main_func()
