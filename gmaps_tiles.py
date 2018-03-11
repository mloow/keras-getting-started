import sys
import os
import re
import argparse
import urllib.parse

import numpy as np
from skimage import io
import matplotlib.pyplot as plt
import matplotlib

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
parser.add_argument('-c', '--center', nargs=1,
                    help='Map center in longitude and latitude given as lon,lat or a city name. Use double-quotes if the city contains spaces')
parser.add_argument('-k', '--key', nargs=1, required=True,
                     help='Google API key')
parser.add_argument('-z', '--zoom', nargs=1, type=int, default=15,
                    help='Map zoom level (1: world, 5: landmass/continent, 10: city, 15: streets, 20: buildings)')
parser.add_argument('-s', '--size', nargs=2, type=int, default=[512, 512], metavar=('w', 'h'),
                    help='Map dimension in pixels, in width and height')
parser.add_argument('-n', '--num-tiles', nargs=1, type=int, default=8,
                    help='Number of tiles per dimension')
parser.add_argument('-p', '--plot', default=None, choices=['original', 'tiles', 'both', None],
                    help='Display the downloaded static map')
parser.add_argument('-d', '--dir', nargs=1, type=str,
                    help='Output directory')
parser.add_argument('--no-save', action='store_true',
                    help='Do not save the resulting tiles')

args = parser.parse_args()

if args.center is None:
    center = input()
else:
    center = args.center[0]
center = center.strip()
center = re.sub('\s*,\s*', ',', center)
center = re.sub('\s+', '+', center)

if args.size[0] % args.num_tiles[0] != 0:
    sys.exit('Width ({}) is not divisible by number of tiles ({})!'.format(args.size[0], args.num_tiles[0]))
if args.size[1] % args.num_tiles[0] != 0:
    sys.exit('Height ({}) is not divisible by number of tiles ({})!'.format(args.size[1], args.num_tiles[0]))
if not re.fullmatch('(-?\d+(\.\d+)?,-?\d+(\.\d+)?)|([\w,\s]*)', center):
    sys.exit('\'{}\' is not a valid value for location!'.format(center))
if not args.dir:
    args.dir = []
    args.dir.append(center + '_out')
if not re.fullmatch('[/\w\.]+', args.dir[0]):
    sys.exit('\'{}\' is not a valid path!'.format(args.dir[0]))

watermark_h = 20
args.size[1] = args.size[1] + watermark_h
size = 'x'.join(list(map(str, args.size)))

url_vars = {'center': center,
            'zoom': args.zoom,
            'size': size,
            'maptype': 'satellite',
            'key': args.key[0]}

base_url = 'https://maps.googleapis.com/maps/api/staticmap?'
url = base_url + urllib.parse.urlencode(url_vars)
static_map = io.imread(url)
static_map = np.array(static_map)
static_map = static_map[:][:-watermark_h][:]
tiles = tile_image(static_map, args.num_tiles[0])

if not args.no_save and not os.path.exists(args.dir[0]):
    os.makedirs(args.dir[0])

for row in range(args.num_tiles[0]):
    for col in range(args.num_tiles[0]):
        index = row * args.num_tiles[0] + col
        if not args.no_save:
            fname = '{}/{}_{}.png'.format(args.dir[0], center, index)
            matplotlib.image.imsave(fname, tiles[index])
        if args.plot == 'tiles' or args.plot == 'both':
            plt.subplot(args.num_tiles[0], args.num_tiles[0], index + 1)
            plt.imshow(tiles[index])    

if args.plot == 'original' or args.plot == 'both' or args.no_save:
    plt.imshow(static_map)
    plt.show()

if args.plot == 'tiles' or args.plot == 'both':
    plt.show()
