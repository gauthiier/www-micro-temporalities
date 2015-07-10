#!/usr/bin/python2.7

import sys, csv, json, os, re
from optparse import OptionParser

def run(csv_file_path):

	if not os.path.exists(csv_file_path):
		sys.exit('Input file does not exists. Aborting.')

	stats = {
	'date' : None,
	'time' : None,
	'host' : None,
	'items' : {'ad': 0.0, 'tracker': 0.0, 'analytics': 0.0, 'widget': 0.0, 'privacy': 0.0, '-': 0.0, 'total' : 0.0},
	'sizes' : {'ad': 0.0, 'tracker': 0.0, 'analytics': 0.0, 'widget': 0.0, 'privacy': 0.0, '-': 0.0},
	'times' : {'ad': 0.0, 'tracker': 0.0, 'analytics': 0.0, 'widget': 0.0, 'privacy': 0.0, '-': 0.0}
	}

	with open(csv_file_path) as csv_file:
		wpt_data = csv.DictReader(csv_file)
		items = stats['items']
		sizes = stats['sizes']
		times = stats['times']
		for d in wpt_data:
			if not stats['host']:
				stats['host'] = d['Host'] # first line
				stats['date'] = d['Date'] # first line
				stats['time'] = d['Time'] # first line
			items['total'] += 1
			bug_type = d['bug_type']
			items[bug_type] += 1
			sizes[bug_type] += int(d['Object Size'])
			times[bug_type] += int(d['Time to Load (ms)'])

	return stats

if __name__ == '__main__':

	p = OptionParser();
	p.add_option('-f', '--file', action="store", help="wpt csv input file")

	options, args = p.parse_args()

	if not options.file:
		sys.exit('No wpt csv input file specified. Aborting.')

	stats = run(options.file)
	print json.dumps(stats, indent=2, separators=(',',':'))
