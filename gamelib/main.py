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
import background_tile

def main():
	print "Hello from your game's main()"
	print data.load('sample.txt').read()

	#setup window
	pygame.init()
	pygame.display.set_mode((640, 480), pygame.OPENGL | pygame.DOUBLEBUF)
	rabbyt.set_viewport((0, 0, 640, 480), (0, 0, 640, 480))
	rabbyt.set_default_attribs()
	clock = pygame.time.Clock()

	p = player.Player()

	floor = create_level()

	#the gameloop
	keepRunning = True

	while keepRunning:
		clock.tick()

		events = pygame.event.get()

		for event in events:
			if event.type == QUIT:
				keepRunning = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					keepRunning = False

		key_downs = [e for e in events if e.type == KEYDOWN]
		keys_pressed = pygame.key.get_pressed()
		p.handle_input(key_downs, keys_pressed)

		p.update(floor)

		#the actual rendering code
		rabbyt.clear((0.2, 0.2, 0.2)) #clear the screen
		rabbyt.render_unsorted([t.sprite for t in floor])
		p.sprite.render() #render the sprite

		pygame.display.flip() #flip the buffers

def create_level():
	floor = [background_tile.Tile((x, 480)) for x in range(0, 640, 32)]
	floor.extend([background_tile.Tile((x, 480-32)) for x in range(320, 640, 32)])
	floor.extend([background_tile.Tile((x, 480-32)) for x in range(0, 32*4, 32)])
	return floor
