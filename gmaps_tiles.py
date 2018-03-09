import sys
import argparse
import re
import urllib.parse

base_url = 'https://maps.googleapis.com/maps/api/staticmap?'

parser = argparse.ArgumentParser()
parser.add_argument('center', nargs=1,
                    help='Map center in longitude and latitude given as lon,lat or a city name in quotes')
parser.add_argument('key', nargs=1,
                     help='Google API key')
parser.add_argument('-z', '--zoom', nargs=1, type=int, default=15,
                    help='Map zoom level (1: world, 5: landmass/continent, 10: city, 15: streets, 20: buildings)')
parser.add_argument('-s', '--size', nargs=2, type=int, default=[512, 512], metavar=('w', 'h'),
                    help='Map dimension in pixels given as width and height')
parser.add_argument('-n', '--num-tiles', nargs=1, type=int, default=8,
                    help='Number of tiles per dimension')

args = parser.parse_args()

if not re.fullmatch('(-?\d+(\.\d+)?,\d+(\.\d+)?)|([a-zA-Z](\s*,?\s*\w+)*)', args.center[0]):
    sys.exit('\'{}\' is not a valid value for location!'.format(args.center[0]))

center = args.center[0]
center = re.sub('\s*,\s*', ',', center)
center = re.sub('\s+', '+', center)

size = 'x'.join(list(map(str, args.size)))

url_vars = {'center': center,
            'zoom': str(args.zoom),
            'size': size,
            'maptype': 'satellite',
            'key': args.key[0]}

url = base_url + urllib.parse.urlencode(url_vars)
print(url)