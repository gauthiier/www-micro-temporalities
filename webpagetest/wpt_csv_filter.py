#!/usr/bin/python2.7

import sys, csv, json, os, re
from optparse import OptionParser

# list of fileds from the wpt csv file to keep
csv_fields = [
'Date',
'Time',
'bug_type',
'bug_name',
'Sequence Number',
'Host',
'IP Address', 
'URL',
'Action',
'Response Code',
'Content Type',
'Content Encoding',
'CDN Provider',
'Connect Time',
'Time to Load (ms)',
'Time to First Byte (ms)',
'Real Start Time (ms)',
'Start Time (ms)',
'End Time (ms)',
'Full Time to Load (ms)',
'DNS Time',
'DNS Start',
'DNS End',
'SSL Time',
'SSL Negotiation Start',
'SSL Negotiation End',
'Connect Start',
'Connect End',
'Object Size',
'Bytes In',
'Bytes Out',
'Image Total Bytes',
'Initiator',
'Initiator Line',
'Expires',
'Cached',
'Cookie Count(out)'
 ]

# matches a given url to all possible bugs
def match(url, bugs):
	for b in bugs:
		pattern = re.compile(b['pattern'])
		if(pattern.search(url)):
			return {'name': b['name'], 'type': b['type'], }
	return None

# filters the csv file (deleted some columns) and adds the 'tracker type'
def filter_fields(wpt_row, type, name):
	for k in wpt_row.keys():
		if k not in csv_fields:
			del wpt_row[k]
	wpt_row['bug_type'] = type
	wpt_row['bug_name'] = name

def run(options):

	if not options.file:
		sys.exit('No wpt csv input file specified. Aborting.')

	csv_file = options.file

	if not options.bugs:
		sys.exit('No ghostery (formated) bugs input file. Aborting.')

	bugs_file = options.bugs

	try:
		wpt_data = csv.DictReader(open(csv_file))
	except Exception, ee:	
		sys.exit('Error loading wpt csv data... Aborting.')

	try:
		with open(bugs_file) as bugs_data_file:
			bugs_data = json.load(bugs_data_file)
	except Exception, ee:	
		sys.exit('Error loading bugs data... Aborting.')

	#write ouput 
	fname, ext = os.path.splitext(os.path.basename(csv_file))

	if not os.path.exists(options.outputdir):
		os.makedirs(options.outputdir)

	out_csv_filename =  options.outputdir + fname + "__filtered" + ext

	out_csv = open(out_csv_filename, 'w')
	writer = csv.DictWriter(out_csv, fieldnames=csv_fields)
	writer.writeheader()

	last_seq = 0

	for r in wpt_data:
		seq = int(r['Sequence Number'])
		if  seq < last_seq:
			break
		last_seq = seq

		print str(seq)

		url = r['Host'] + r['URL']
		bug = match(url, bugs_data['bugs'])
		if bug:
			filter_fields(r, bug['type'], bug['name'])
			writer.writerow(r);
		else:
			if options.keep:
				filter_fields(r, '-', '-')
				writer.writerow(r);

if __name__ == '__main__':

	p = OptionParser();
	p.add_option('-f', '--file', action="store", help="wpt csv input file")
	p.add_option('-b', '--bugs', action="store", help="ghostery (formated) bugs input file")
	p.add_option('-k', '--keep', action="store_true", help="keeps the non bugs html element")
	p.add_option('-o', '--outputdir', action="store", help="output directory", default="")


	options, args = p.parse_args()

	run(options)







