import sys
import data
#import rabbyt
#from rabbyt.primitives import Quad
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
		self.sprite_sheet = pygame.image.load(data.filepath("scientist.png"))
		self.f_sprite_sheet = pygame.transform.flip(self.sprite_sheet, True, False)

		self.direction = FACING_LEFT
		self.ambulatory_state = STANDING
		self.y_vel = 0
		self.x_vel = 0
		self.x = 20
		self.y = 300 # initial position
		self.w = 32
		self.h = 64
		self.frame = 8
		self.update_bottom_surface()

	def update_bottom_surface(self):
		mid_x = self.x + self.w / 2
		surface_width = 8
		self.bottom_surface = pygame.Rect(
			mid_x - surface_width / 2, self.y + 63,
			surface_width, 1
			)

	def stand_still(self):
		self.ambulatory_state = STANDING
		self.x_vel = 0

	def move_left(self):
		if self.ambulatory_state != JUMPING:
			self.ambulatory_state = RUNNING
		if self.direction != FACING_LEFT:
			self.direction = FACING_LEFT
		self.x_vel = max(self.x_vel - RUN_ACCEL, -TOP_SPEED)

	def move_right(self):
		if self.ambulatory_state != JUMPING:
			self.ambulatory_state = RUNNING
		if self.direction != FACING_RIGHT:
			self.direction = FACING_RIGHT
		self.x_vel = min(self.x_vel + RUN_ACCEL, TOP_SPEED)

	def jump(self):
		'''BOING!'''
		if self.ambulatory_state == JUMPING:
			# no double jumps!
			return
		self.ambulatory_state = JUMPING
		self.y_vel = JUMP_FORCE

	def check_platforms(self, platforms):
		if self.y_vel < 0:
			return
		self.update_bottom_surface()
		collision = self.bottom_surface.collidelist(platforms)
		
		if collision != -1:
			# landed on something
			self.ambulatory_state = STANDING
			self.y = platforms[collision].top - 64
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

	def update(self, platforms):
		if self.ambulatory_state == RUNNING:
			self.frame = ((int(self.x) >> 3) % 8) + 0
			if self.direction == FACING_LEFT:
				self.frame = 7 - self.frame  # otherwise sprite appears to moon-walk	
		elif self.ambulatory_state == STANDING:
			self.frame = 8
		elif self.ambulatory_state == JUMPING:
			self.frame = 1

		self.y += self.y_vel
		self.x += self.x_vel

		self.y_vel += GRAVITY_ACCEL

		if self.y_vel > 1:
			self.ambulatory_state = JUMPING # falling really

		self.check_platforms(platforms)

		# print i
		#t_x = i / 15.0
		#self.sprite.tex_shape.left = t_x
		#self.sprite.tex_shape.bottom = 1

	def render(self, surface):
		if self.direction == FACING_RIGHT:
			sprite_sheet_to_use = self.f_sprite_sheet
			frame_to_use = 14 - self.frame
		else:
			sprite_sheet_to_use = self.sprite_sheet # flipped version
			frame_to_use = self.frame
		surface.blit(sprite_sheet_to_use, (self.x, self.y), (frame_to_use*self.w, 0, self.w, self.h))
