'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''

#import rabbyt
import sys
import json
import math
import pygame
from pygame.locals import *
import player
import data
#import background_tile
import tiledmap

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

def main():

	print "Hello from your game's main()"
	print data.load('sample.txt').read()

	#setup window
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
	#rabbyt.set_viewport((0, 0, 640, 480), (0, 0, 640, 480))
	#rabbyt.set_default_attribs()

	screen_buf = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
	bg = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
	clock = pygame.time.Clock()

	print "Loading tile map..."
	#tiledmap = json.loads(data.load("level_map.json").read())
	#print json.dumps(tiledmap, indent=2)
	#sys.exit(0)

	p = player.Player()

	level_map = tiledmap.TiledRenderer()
	level_map.render(bg)

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

		p.update(level_map.platforms)

		screen_buf.blit(bg, (0, 0))
		p.render(screen_buf)

		screen.blit(screen_buf, (0, 0))
		pygame.display.flip() #flip the buffers

def create_level():
	floor = [background_tile.Tile((x, 480)) for x in range(0, 640, 32)]
	floor.extend([background_tile.Tile((x, 480-32)) for x in range(320, 640, 32)])
	floor.extend([background_tile.Tile((x, 480-32)) for x in range(0, 32*4, 32)])
	return floor
