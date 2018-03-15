import sys
import os

key = sys.argv[1]

cities = ['stockholm',
          'göteborg',
          'malmö',
          'uppsala']

villages = ['björkå',
            'lillskog',
            'munkbyn',
            'sörskog']

cities = [('city', center) for center in cities]
villages = [('village', center) for center in villages]
centers = cities + villages


for (label, center) in centers:
	print('Downloading maps over {} {}'.format(label, center))
	os.system('python gmaps_tiles.py --key {} --size 256 256 --center {} --dir {}'.format(key, center, label))

for label in ['city', 'village']:
	print('Applying lbp to {} maps'.format(label))
	os.system('python imfunc.py --lbp 8 1 -d {} -o samples.csv -a -l {}'.format(label, label))
