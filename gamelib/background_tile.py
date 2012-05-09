import data
#import rabbyt
import math
#from rabbyt.primitives import Quad
from pygame.sprite import Sprite
import pygame
from pygame.locals import *

TILE_WIDTH = 32
TILE_HEIGHT = 32

class Tile(object):
	def __init__(self, (x_pos, y_pos)):
		#load our self.sprite
		self.sprite = rabbyt.Sprite(data.filepath("tile.png"))
		self.sprite.shape = (0, -32, 32, 0)
		self.sprite.x = x_pos
		self.sprite.y = y_pos
		self.top_surface = Quad((self.sprite.left,
			self.sprite.bottom,
			self.sprite.right,
			self.sprite.bottom+5))

