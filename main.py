import sys, pygame, chip8
from pygame import gfxdraw
pygame.init()

#Variables
def main_func():
	my_chip8 = chip8.Chip8()
	black = 0,0,0
	white = 255,255,255
	colors = [black, white]
	size = width, height = 64 , 32
	pixels = width * height
	
	
	screen = pygame.display.set_mode(size)

	#Set up emulation system
	setup_graphics(screen)
	setup_input()

	#Initialize chip8 system
	my_chip8.initialize(pixels)
	my_chip8.load_game("pong.c8")

	#Emulation Loop
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

		my_chip8.emulate_cycle()

		if(my_chip8.draw_flag):
			draw_graphics(screen, colors, my_chip8, width, height)
		
		my_chip8.set_keys()

def setup_graphics(screen):
	screen.fill((0,0,0))

def setup_input():
	pass

def draw_graphics(screen, colors, my_chip8, width, height):
	for x in range(width):
		for y in range(height):
			gfxdraw.pixel(screen, x, height - y, colors[my_chip8.graphics[x + (y * width)]])

	pygame.display.flip()
	my_chip8.draw_flag = False

if __name__ == "__main__":
	main_func()