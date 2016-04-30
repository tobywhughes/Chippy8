from array import array

class Chip8:

	def __init__(self):
		self.fontset = array('H', 
 		[0xF0, 0x90, 0x90, 0x90, 0xF0, 
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
	    0xF0, 0x80, 0xF0, 0x80, 0x80])

	def initialize(self, pixels):
		self.stack = []
		self.opcode = 0
		self.memory = [0] * 4096
		self.pc = 0x200
		self.I = 0
		self.sp = 0
		self.V = [0] * 16
		#Init clear screen
		self.graphics = [0] * pixels

		#Fontset
		for i in range(80):
			self.memory[i] = self.fontset[i]

		self.draw_flag = True

	def load_game(self, file_name):
		with open(file_name, "rb") as f:
			byte = f.read()
			for i in range(len(byte)):
				self.memory[self.pc + i] = byte[i]

	def emulate_cycle(self):
		#Gets opcode
		self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]
		print(hex(self.opcode))
		print(hex(self.pc))
		#Decodes opcode
		#1NNN
		if(self.opcode & 0xF000 == 0x1000):
			self.pc = self.opcode & 0x0FFF

		#2NNN
		elif(self.opcode & 0xF000 == 0x2000):
			self.stack.append(self.pc)
			self.pc = self.opcode & 0x0FFF

		#3XNN
		elif(self.opcode & 0xF000 == 0x3000):
			x = self.opcode & 0x0F00 >> 8
			if self.V[x] == self.opcode & 0x00FF:
				self.pc += 2
			self.pc += 2
		
		#4XNN
		elif(self.opcode & 0xF000 == 0x4000):
			x = self.opcode & 0x0F00 >> 8
			if self.V[x] != self.opcode & 0x00FF:
				self.pc += 2
			self.pc += 2

		#6XNN
		elif(self.opcode & 0xF000 == 0x6000):
			x = self.opcode & 0x0F00 >> 8
			self.V[x] = self.opcode & 0x00FF
			self.pc += 2
		
		#7XNN
		elif(self.opcode & 0xF000 == 0x7000):
			x = self.opcode & 0x0F00 >> 8
			self.V[x] += self.opcode & 0x00FF
			print(self.V[x])
			self.pc += 2

		#ANNN
		elif(self.opcode & 0xF000 == 0xA000):
			self.I = self.opcode & 0x0FFF
			self.pc += 2

		#DXYN
		elif(self.opcode & 0xF000 == 0xD000):
			xcord = self.V[self.opcode & 0x0F00 >> 8] 
			ycord = self.V[self.opcode & 0x00F0 >> 4]
			height = self.opcode & 0x000F
			pixel = 0
			self.V[0xF] = 0

			for y in range(height):
				pixel = self.memory[self.I + y]
				for x in range(8):
					i = xcord + x + ((y + ycord) * 64)
					if pixel & (0x80 >> x) != 0 and not (y + ycord >= 32 or x + xcord - 1 >= 64):
						if self.graphics[i] == 1:
							self.V[0xF] = 1
						self.graphics[i] ^= 1

			self.pc += 2
			self.draw_flag = True

		
		#Not currently made print
		else:
			print(hex(self.opcode))

	def set_keys(self):
		pass

if __name__ == "__main__":
	from main import main_func
	main_func()
