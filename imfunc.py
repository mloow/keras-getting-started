import argparse
import os
import csv
import numpy as np
from skimage.feature import local_binary_pattern
from skimage import io
from skimage.color import rgb2grey

parser = argparse.ArgumentParser()
parser.add_argument('--lbp', 
	                nargs=2, 
	                metavar=('neighbors', 'radius'),
	                default=[8, 1])
parser.add_argument('-d', '--dir', default='.', help='Image source directory')
parser.add_argument('-o', '--output', default='out.csv', help='Output file')
parser.add_argument('-a', '--append', action='store_true', help='Append output to output file')
parser.add_argument('-l', '--label', nargs=1, default='no_label', help='A label to give the output')

args = parser.parse_args()
results = {}

for filename in os.listdir(args.dir):
	img = io.imread(args.dir + '/' + filename)
	if args.lbp:
		lbp = local_binary_pattern(rgb2grey(img), int(args.lbp[0]), int(args.lbp[1]), 'uniform')
		nbins = int(args.lbp[0]) + 2
		(counts, _) = np.histogram(lbp, bins=nbins)
		rel_freq = list(map(lambda x: x / np.product(lbp.shape), counts))
		results[os.path.abspath(filename)] = rel_freq

with open(args.output, 'a' if args.append else 'w', encoding='utf-8', newline='') as f:
	writer = csv.writer(f, delimiter=',')
	for key, res in results.items():
		writer.writerow([key] + [args.label[0]] + res)
f.close()
