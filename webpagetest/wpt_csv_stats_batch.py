import sys, csv, json, os, re
from optparse import OptionParser
import wpt_csv_stats

def run(input_dir):

	if not os.path.exists(input_dir):
		sys.exit('Input directory does not exists. Aborting.')

	stats = []

	csv_files = []
	for (dirpath, dirnames, filenames) in os.walk(input_dir):
		for fn in filenames:
			fname, ext = os.path.splitext(fn)
			if ext == '.csv':
				filepath = os.path.join(dirpath, fn)
				stats.append({'name' : fname, 'stats': wpt_csv_stats.run(filepath)})
		break

	return stats

if __name__ == '__main__':

	p = OptionParser();
	p.add_option('-i', '--inputdir', action="store", help="input directory (where all the wpt csv files reside)")

	options, args = p.parse_args()

	if not options.inputdir:
		sys.exit('No input directory specified. Aborting.')

	stats = run(options.inputdir)
	print json.dumps(stats, indent=2, separators=(',',':'))
