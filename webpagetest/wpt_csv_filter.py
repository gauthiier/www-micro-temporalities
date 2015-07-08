#!/usr/bin/python2.7

import sys, csv, json, os
from optparse import OptionParser

# list of fileds from the wpt csv file to keep
csv_fields = [
'Date',
'Time',
'tracker_type',
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
'Cookie Count(out)',
 ]

def filter_fields(wpt_row, type):
	for k in wpt_row.keys():
		if k not in csv_fields:
			del wpt_row[k]
	wpt_row['tracker_type'] = type

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

	stats = {'total' : 0.0, 'ads': 0.0, 'trackers': 0.0, 'analytics': 0.0, 'widgets': 0.0, 'privacy': 0.0, 'blank': 0.0}

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
		stats['total'] += 1
		host = r['Host']
		if any(a in host for a in bugs_data['ads']):
#			print "ads: " + host
			filter_fields(r, 'ad')
			writer.writerow(r);
			stats['ads'] += 1
			continue
		if any(a in host for a in bugs_data['trackers']):
#			print "trackers: " + host
			filter_fields(r, 'tracker')
			writer.writerow(r);
			stats['trackers'] += 1
			continue
		if any(a in host for a in bugs_data['analytics']):
#			print "analytics: " + host
			filter_fields(r, 'analytics')
			writer.writerow(r);
			stats['analytics'] += 1
			continue
		if any(a in host for a in bugs_data['widgets']):
#			print "widgets: " + host
			filter_fields(r, 'widget')
			writer.writerow(r);
			stats['widgets'] += 1
			continue
		if any(a in host for a in bugs_data['privacy']):
#			print "privacy: " + host
			filter_fields(r, 'privacy')
			writer.writerow(r);
			stats['privacy'] += 1
			continue			
		if options.keep:
			stats['blank'] += 1
			filter_fields(r, '-')
			writer.writerow(r);


	if options.stats:
		print "----- Stats: " + fname + ext + " -----"
		print "total (elements): " + str(stats['total'])
		print "ads: " + str(stats['ads']) + ' - ' + str(stats['ads'] / stats['total']) + '%'
		print "trackers: " + str(stats['trackers']) + ' - ' + str(stats['trackers'] / stats['total']) + '%'
		print "analytics: " + str(stats['analytics']) + ' - ' + str(stats['analytics'] / stats['total']) + '%'
		print "widgets: " + str(stats['widgets']) + ' - ' + str(stats['widgets'] / stats['total']) + '%'
		print "privacy: " + str(stats['privacy']) + ' - ' + str(stats['privacy'] / stats['total']) + '%'
		print "..............."
		print "* JUNK RATIO * " + str((stats['ads'] + stats['trackers'] + stats['analytics'] + stats['widgets'] + stats['privacy']) / stats['total']) + '%'			

if __name__ == '__main__':

	p = OptionParser();
	p.add_option('-f', '--file', action="store", help="wpt csv input file")
	p.add_option('-b', '--bugs', action="store", help="ghostery (formated) bugs input file")
	p.add_option('-k', '--keep', action="store_true", help="keeps the non bugs html element")
	p.add_option('-s', '--stats', action="store_true", help="prints basic stats")
	p.add_option('-o', '--outputdir', action="store", help="output directory", default="")


	options, args = p.parse_args()

	run(options)







