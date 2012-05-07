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
TOP_SPEED = 1  # fastest run
TERMINAL_VELOCITY = 10  # top speed falling
RUN_ACCEL = 0.1
GRAVITY_ACCEL = 0.2
JUMP_FORCE = -4

class Player(object):
	def __init__(self):
		#load our self.sprite
		self.sprite = rabbyt.Sprite(data.filepath("scientist.png"))
		self.sprite.shape = (-16, -64, 16, 0)
		self.sprite.tex_shape.width, self.sprite.tex_shape.height = 1/15.0, 1
		self.direction = FACING_LEFT
		self.ambulatory_state = STANDING
		self.y_vel = 0
		self.x_vel = 0
		self.sprite.y = 480 - 32 # initial position
		self.update_bottom_surface()

	def update_bottom_surface(self):
		x, y = self.sprite.x, self.sprite.y
		self.bottom_surface = Quad((x-6, y-1, x+6, y))

	def stand_still(self):
		self.ambulatory_state = STANDING
		self.x_vel = 0

	def move_left(self):
		if self.ambulatory_state != JUMPING:
			self.ambulatory_state = RUNNING
		if self.direction != FACING_LEFT:
			self.sprite.scale_x = 1
			self.direction = FACING_LEFT
		self.x_vel = max(self.x_vel - RUN_ACCEL, -TOP_SPEED)

	def move_right(self):
		if self.ambulatory_state != JUMPING:
			self.ambulatory_state = RUNNING
		if self.direction != FACING_RIGHT:
			self.sprite.scale_x = -1
			self.direction = FACING_RIGHT
		self.x_vel = min(self.x_vel + RUN_ACCEL, TOP_SPEED)

	def jump(self):
		'''BOING!'''
		if self.ambulatory_state == JUMPING:
			# no double jumps!
			return
		self.ambulatory_state = JUMPING
		self.y_vel = JUMP_FORCE

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
			# landed on something
			self.ambulatory_state = STANDING
			self.sprite.y = collisions[0].bottom
			self.y_vel = 0

	def handle_input(self, key_downs, keys_pressed):
		# key_downs handles key events that should be handled once,
		# such as shooting and jumping.


		# keys_pressed handles events for the duration that they are 'pressed'
		# such has running or climbing.
		if keys_pressed[K_LEFT]:
			self.move_left()
		if keys_pressed[K_RIGHT]:
			self.move_right()
		if ((keys_pressed[K_RIGHT] == keys_pressed[K_LEFT])
			and self.ambulatory_state != JUMPING):
			# ie: both directions pressed OR niether pressed
			self.stand_still()

		for event in key_downs:
			if event.key == K_UP:
				self.jump()

	def update(self, floor):
		if self.ambulatory_state == RUNNING:
			i = ((int(self.sprite.x) >> 3) % 8) + 0
			if self.direction == FACING_LEFT:
				i = 7 - i  # otherwise sprite appears to moon-walk	
		elif self.ambulatory_state == STANDING:
			i = 8
		elif self.ambulatory_state == JUMPING:
			i = 1

		self.sprite.y += self.y_vel
		self.sprite.x += self.x_vel

		self.y_vel += GRAVITY_ACCEL

		if self.y_vel > 1:
			self.ambulatory_state = JUMPING # falling really

		self.check_floor(floor)

		# print i
		t_x = i / 15.0
		self.sprite.tex_shape.left = t_x
		self.sprite.tex_shape.bottom = 1
