'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

import rabbyt
import math
import pygame
from pygame.locals import *
import player
import data

def main():
	print "Hello from your game's main()"
	print data.load('sample.txt').read()

	#setup window
	rabbyt.init_display(size=(640, 480))
	rabbyt.set_viewport((640, 480))

	p = player.Player()

	#the gameloop
	keepRunning = True

	while keepRunning:
		#messagepump
		for event in pygame.event.get():
			if event.type == QUIT:
				keepRunning = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					keepRunning = False
				if event.key == K_UP:
					print "JUMP KEY PRESSED"
					p.jump()
		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[K_LEFT]:
			p.move_left()
		if pressed_keys[K_RIGHT]:
			p.move_right()
		if not(pressed_keys[K_RIGHT] or pressed_keys[K_LEFT]):
			p.stand_still()

		#the actual rendering code
		rabbyt.clear() #clear the screen

		p.sprite.render() #render the sprite

		pygame.display.flip() #flip the buffers

