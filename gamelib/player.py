import sys
import data
import rabbyt
from rabbyt.primitives import Quad
import math
import pygame
from pygame.locals import *


FACING_LEFT = object()
FACING_RIGHT = object()
RUNNING = object()
STANDING = object()
JUMPING = object()

class Player(object):
	def __init__(self):
		#load our self.sprite
		self.sprite = rabbyt.Sprite(data.filepath("ninja_basic.png"))
		self.sprite.shape = (-16, -64, 16, 0)
		self.sprite.tex_shape.width, self.sprite.tex_shape.height = 1/10.0, 1
		self.direction = FACING_RIGHT
		self.ambulatory_state = STANDING
		self.y_vel = 0
		self.sprite.y = 480 - 32 # initial position
		self.update_bottom_surface()

	def update_bottom_surface(self):
		x, y = self.sprite.x, self.sprite.y
		self.bottom_surface = Quad((x-16, y-1, x+16, y))

	def stand_still(self):
		pass

	def move_left(self):
		if self.ambulatory_state != JUMPING:
			self.ambulatory_state = RUNNING
		if self.direction != FACING_LEFT:
			self.sprite.scale_x = -1
			self.direction = FACING_LEFT
		self.sprite.x -= 2

	def move_right(self):
		if self.ambulatory_state != JUMPING:
			self.ambulatory_state = RUNNING
		if self.direction != FACING_RIGHT:
			self.sprite.scale_x = 1
			self.direction = FACING_RIGHT
		self.sprite.x += 2

	def jump(self):
		'''BOING!'''
		if self.ambulatory_state == JUMPING:
			# no double jumps!
			return
		self.ambulatory_state = JUMPING
		self.y_vel = -10

	def check_floor(self, floor_tiles):
		if self.y_vel < 0:
			return
		self.update_bottom_surface()
		collisions = rabbyt.collisions.aabb_collide_single(
			self.bottom_surface,
			[t.top_surface for t in floor_tiles]
			)
		# print collisions
		if collisions:
			self.ambulatory_state = STANDING
			self.sprite.y = collisions[0].top
			self.y_vel = 0

	def update(self, floor):
		if self.ambulatory_state == RUNNING:
			i = ((int(self.sprite.x) >> 3) % 4) + 2
		elif self.ambulatory_state == STANDING:
			i = 0
		else:
			i = 1
		self.sprite.y += self.y_vel
		self.y_vel += 1

		self.check_floor(floor)

		#if self.sprite.y >= 480 - 32:
		#	self.y_vel = 0
		#	self.sprite.y = 480 - 32
		#	self.ambulatory_state = STANDING
		#	self.i = 0
		
		print i
		t_x = i / 10.0
		self.sprite.tex_shape.left = t_x
		self.sprite.tex_shape.bottom = 1
