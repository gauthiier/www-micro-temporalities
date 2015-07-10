#!/usr/bin/python2.7

import sys, csv, json, os, time
from optparse import OptionParser
import wpt_csv_filter as wptf

class option:
    pass

def run(options):

	if not options.inputdir:
		sys.exit('No input directory specified. Aborting.')

	if not options.bugs:
		sys.exit('No ghostery (formated) bugs input file. Aborting.')

	if not os.path.exists(options.inputdir):
		sys.exit('Input directory does not exists. Aborting.')

	if not os.path.exists(options.outputdir):
		os.makedirs(options.outputdir)

	out = options.inputdir
	csv_files = []
	for (dirpath, dirnames, filenames) in os.walk(out):
		for fn in filenames:
			fname, ext = os.path.splitext(fn)
			if ext == '.csv':
				csv_files.append(os.path.join(dirpath, fn))
		break

	i = 0
	for f in csv_files:
		i += 1
		options.file = f
		print str(i) + "/" + str(len(csv_files)) + " - " + f
		start_time = time.time()
		wptf.run(options)
		duration = time.time() - start_time
		print "done - " + time.strftime('%H:%M:%S', time.gmtime(duration))

if __name__ == '__main__':

	p = OptionParser();
	p.add_option('-i', '--inputdir', action="store", help="input directory (where all the wpt csv files reside)")
	p.add_option('-b', '--bugs', action="store", help="ghostery (formated) bugs input file")
	p.add_option('-k', '--keep', action="store_true", help="keeps the non bugs html element")
	p.add_option('-o', '--outputdir', action="store", help="output directory (where all the filtered csv files will be placed in)", default="")

	options, args = p.parse_args()

	run(options)
