import sys, pygame, chip8
from pygame import gfxdraw, Rect
pygame.init()

#Variables
def main_func():
	keys=[pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, 
              pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r,
              pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f,
	      pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v]
	my_chip8 = chip8.Chip8()
	black = 0,0,0
	white = 255,255,255
	colors = [black, white]
	width, height = 64 , 32
	size = width * 10, height * 10
	pixels = width * height
	
	
	screen = pygame.display.set_mode(size)

	#Set up emulation system
	setup_graphics(screen)

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
		
		events = pygame.event.get()	
		get_key_event(events, keys, my_chip8)

def setup_graphics(screen):
	screen.fill((0,0,0))

def get_key_event(events, keys, my_chip8):
	for event in events:
		event_type = -1
		if event.type == pygame.KEYDOWN:
			event_type = 1	
		elif event.type == pygame.KEYUP:
			event_type = 0
		if event_type != -1:
			print(event.key)
			if event.key in keys:
				i = keys.index(event.key)
				my_chip8.keys[i] = event_type
		 

def draw_graphics(screen, colors, my_chip8, width, height):
	for x in range(width):
		for y in range(height):
			screen.fill(colors[my_chip8.graphics[x + (y * width)]], Rect(x*10, y*10, 10, 10))

	pygame.display.flip()
	my_chip8.draw_flag = False

if __name__ == "__main__":
	main_func()
