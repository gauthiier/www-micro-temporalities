import sys, csv, json, os
from optparse import OptionParser

# list of fileds from the wpt csv file to keep
csv_fields = ['Connect Time', 'Time to Load (ms)', 'Time to First Byte (ms)', 'Content Type', 'DNS Time', 'Real Start Time (ms)', 'Full Time to Load (ms)', 'Expires', 'Cached', 'Host', 'DNS Start', 'SSL Time', 'Date', 'SSL Negotiation Start', 'Connect End', 'Initiator', 'Image Total Bytes', 'Start Time (ms)', 'URL', 'Content Encoding', 'Cookie Count(out)', 'Bytes In', 'Initiator Line', 'Bytes Out', 'Descriptor', 'Connect Start', 'Time', 'Action', 'Sequence Number', 'CDN Provider', 'DNS End', 'SSL Negotiation End', 'Object Size', 'IP Address', 'End Time (ms)', 'Response Code', 'tracker_type']

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
	out_csv_filename =  fname + "__filtered" + ext

	out_csv = open(out_csv_filename, 'w')
	writer = csv.DictWriter(out_csv, fieldnames=csv_fields)
	writer.writeheader()


	for r in wpt_data:
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
			filter_fields(r, 'n/a')
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
		print "* JUNK INDEX * " + str((stats['ads'] + stats['trackers'] + stats['analytics'] + stats['widgets'] + stats['privacy']) / stats['total']) + '%'	

if __name__ == '__main__':

	p = OptionParser();
	p.add_option('-f', '--file', action="store", help="wpt csv input file")
	p.add_option('-b', '--bugs', action="store", help="ghostery (formated) bugs input file")
	p.add_option('-k', '--keep', action="store_true", help="keeps the non bugs html element")
	p.add_option('-s', '--stats', action="store_true", help="prints basic stats")

	options, args = p.parse_args()

	run(options)







