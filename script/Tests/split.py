#! /usr/bin/env python3
from subprocess import call

with open('justdata', 'r') as infile:
    hodnoty = infile.readlines()
    print (len(hodnoty))

with open('copy', 'r') as infile, open('newdata', 'w') as outfile:
	cas = infile.readlines()
	print (len(cas))
	for datum, hodnota in zip(cas, hodnoty):
		outfile.write(datum.rsplit(maxsplit=1)[0] + " "  + hodnota )




