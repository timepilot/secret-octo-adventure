import json
import rabbyt
import data
from rabbyt.primitives import Quad

DATA_FILE = "level_map.json"

''' load a tiled map from "TILED" json export file
Due to being simplified for use in a PyWeek project, I am utilising
only a single tileset and a single layer even though Tiled supports multiple '''
class TiledMap(object):
	def __init__(self):
		self.map_data = json.loads(data.load(DATA_FILE).read())
		self.tileset = self.map_data["tilesets"][0]
		self.layer = self.map_data["layers"][0]
		self._load_all_tiles()

	def _load_all_tiles(self):
		self.all_tiles = []
		for i, tile in enumerate(self.layer["data"]):
			if tile == 0:
				continue
			new_tile = Tile(self.map_data, self.tileset, self.layer, tile, i)
			self.all_tiles.append(new_tile)

class Tile(rabbyt.Sprite):
	def __init__(self, map_data, tileset, layer, tile, index):

		file_name = data.filepath(tileset["image"])
		super(self.__class__, self).__init__(file_name)

		num_columns = tileset["imagewidth"] / tileset["tilewidth"]

		w_norm = tileset["tilewidth"] / float(tileset["imagewidth"])
		h_norm = tileset["tileheight"] / float(tileset["imageheight"])
		self.tile_index = tile - 1
		self.tex_shape.width = -w_norm
		self.tex_shape.height = -h_norm
		self.tex_shape.left = (self.tile_index % num_columns) * w_norm
		self.tex_shape.top = 1 - (self.tile_index / num_columns) * h_norm

		self.shape = (tileset["tilewidth"], tileset["tileheight"], 0, 0)

		self.x = (index % layer["width"]) * tileset["tilewidth"]
		self.y = (index / layer["width"]) * tileset["tileheight"]

		self.is_platform = (str(tile-1) in tileset["tileproperties"]
			and "type" in tileset["tileproperties"][str(tile-1)])

		self.top_surface = Quad((self.left,
			self.bottom,
			self.left+32,
			self.bottom+5))


def main():
	tiled_map = TiledMap()

if __name__ == '__main__':
	main()


