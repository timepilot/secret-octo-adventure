import data
import pygame

class TiledRenderer():
	"""
	Super simple way to render a tiled map
	"""

	def __init__(self):
		from PyTMX.pytmx import tmxloader
		filename = data.filepath("level_map.tmx")
		self.tiledmap = tmxloader.load_pygame(filename, pixelalpha=True)
		self.platforms = self.getPlatforms()
 
	def getPlatforms(self):
		platforms = []

		tw = self.tiledmap.tilewidth
		th = self.tiledmap.tileheight
		gp = self.tiledmap.getTileProperties

		for l in xrange(0, len(self.tiledmap.layers)):
			for y in xrange(0, self.tiledmap.height):
				for x in xrange(0, self.tiledmap.width):
					# Check if the tile is a platform
					props = gp((x, y, l))
					if props == None: continue
					if props.get("type", None) == "platform":
						platforms.append(pygame.Rect(x*tw, y*th, tw, 10))
		return platforms

	def render(self, surface):
		# not going for effeciency here
		# for demonstration purposes only

		tw = self.tiledmap.tilewidth
		th = self.tiledmap.tileheight
		gt = self.tiledmap.getTileImage

		for l in xrange(0, len(self.tiledmap.layers)):
			for y in xrange(0, self.tiledmap.height):
				for x in xrange(0, self.tiledmap.width):
					# Draw the tile
					tile = gt(x, y, l)
					if not tile == 0: surface.blit(tile, (x*tw, y*th))

