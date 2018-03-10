import sys
import argparse
import re
import urllib.parse
from skimage import io
import matplotlib.pyplot as plt
import numpy as np

base_url = 'https://maps.googleapis.com/maps/api/staticmap?'

def tile_image(image, num_tiles):
    width_per_tile = int(image.shape[0] / num_tiles)
    height_per_tile = int(image.shape[1] / num_tiles)
    tiles = []
    for i in range(num_tiles):
        for j in range(num_tiles):
            x = i*width_per_tile
            y = j*height_per_tile
            tile = image[x:x + width_per_tile, y:y + height_per_tile]
            tiles.append(tile)
    return tiles

parser = argparse.ArgumentParser()
parser.add_argument('center', nargs=1,
                    help='Map center in longitude and latitude given as lon,lat or a city name in quotes')
parser.add_argument('-k', '--key', nargs=1, required=True,
                     help='Google API key')
parser.add_argument('-z', '--zoom', nargs=1, type=int, default=15,
                    help='Map zoom level (1: world, 5: landmass/continent, 10: city, 15: streets, 20: buildings)')
parser.add_argument('-s', '--size', nargs=2, type=int, default=[512, 512], metavar=('w', 'h'),
                    help='Map dimension in pixels given as width and height')
parser.add_argument('-n', '--num-tiles', nargs=1, type=int, default=8,
                    help='Number of tiles per dimension')
parser.add_argument('-p', '--plot', action='store_true',
                    help='Display the downloaded static map')

args = parser.parse_args()

if args.size[0] % args.num_tiles != 0:
    sys.exit('Width ({}) is not divisible by number of tiles ({})'.format(args.size[0], args.num_tiles))
if args.size[1] % args.num_tiles != 0:
    sys.exit('Height ({}) is not divisible by number of tiles ({})'.format(args.size[1], args.num_tiles))
if not re.fullmatch('(-?\d+(\.\d+)?,\d+(\.\d+)?)|\s*([a-zA-Z](\s*,?\s*\w+)*)', args.center[0]):
    sys.exit('\'{}\' is not a valid value for location!'.format(args.center[0]))

center = args.center[0].strip()
center = re.sub('\s*,\s*', ',', center)
center = re.sub('\s+', '+', center)

size = 'x'.join(list(map(str, args.size)))

url_vars = {'center': center,
            'zoom': args.zoom[0],
            'size': size,
            'maptype': 'satellite',
            'key': args.key[0]}

url = base_url + urllib.parse.urlencode(url_vars)
print(url)
static_map = io.imread(url)
static_map = np.array(static_map)
tiles = tile_image(static_map, args.num_tiles)

if args.plot:
    plt.imshow(static_map)
    plt.show()
    for row in range(args.num_tiles):
        for col in range(args.num_tiles):
            index = row * args.num_tiles + col
            #plt.subplot(args.num_tiles, args.num_tiles, index + 1)
            #plt.imshow(tiles[index])
            #save
    #plt.show()