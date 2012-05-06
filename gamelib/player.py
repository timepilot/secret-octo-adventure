import data
import rabbyt
import math
import pygame
from pygame.locals import *

FACING_LEFT = object()
FACING_RIGHT = object()
RUNNING = object()
STANDING = object()


class Player(object):
	def __init__(self):
		#load our self.sprite
		self.sprite = rabbyt.Sprite(data.filepath("ninja_basic.png"))
		self.sprite.shape.width, self.sprite.shape.height = 32, 64
		self.sprite.tex_shape.width, self.sprite.tex_shape.height = 1/10.0, 1
		self.direction = FACING_RIGHT
		self.ambulatory_state = STANDING

	def stand_still(self):
		if self.ambulatory_state == RUNNING:
			self.ambulatory_state = STANDING
			self.update()

	def move_left(self):
		self.ambulatory_state = RUNNING
		if self.direction != FACING_LEFT:
			self.sprite.scale_x = -1
			self.direction = FACING_LEFT
		self.sprite.x -= 2
		self.update()

	def move_right(self):
		self.ambulatory_state = RUNNING
		if self.direction != FACING_RIGHT:
			self.sprite.scale_x = 1
			self.direction = FACING_RIGHT
		self.sprite.x += 2
		self.update()

	def update(self):
		if self.ambulatory_state == RUNNING:
			i = ((int(self.sprite.x) >> 3) % 4) + 2
		elif self.ambulatory_state == STANDING:
			i = 0
		print i
		t_x = i / 10.0
		self.sprite.tex_shape.left = t_x
		self.sprite.tex_shape.bottom = 1