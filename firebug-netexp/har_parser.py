#!/usr/bin/python2.7

import sys, csv, json, os, re
from optparse import OptionParser

# matches a given url to all possible bugs
def match(url, bugs):
	for b in bugs:
		pattern = re.compile(b['pattern'])
		if(pattern.search(url)):
			return {'name': b['name'], 'type': b['type'], 'class': b['classification']}
	return None

def format(e, b):
	r = {}
	# bug
	r['bug'] = b
	# request
	r['request'] = {}
	r['request']['date_time'] = e['startedDateTime']
	r['request']['time'] = e['time']
	r['request']['method'] = e['request']['method']
	r['request']['url'] = e['request']['url']
	headers = e['request']['headers']
	for h in headers:
		if h['name'] == 'User-Agent':
			r['request']['user_agent'] = h['value']
		elif h['name'] == 'Referer':
			r['request']['referer'] = h['value']
	# response
	r['response'] = {}
	r['response']['status'] = e['response']['status']
	r['response']['server_ip'] = e['serverIPAddress']
	headers = e['response']['headers']
	for h in headers:
		if h['name'] == 'Server':
			r['response']['server_agent'] = h['value']
		if h['name'] == 'Last-Modified':
			r['response']['last_modified'] = h['value']
		if h['name'] == 'Date':
			r['response']['date_time'] = h['value']
	r['response']['header_size'] = e['response']['headersSize']
	r['response']['body_size'] = e['response']['bodySize']
	# content
	r['content'] = {}
	r['content']['mime_type'] = e['response']['content']['mimeType']
	r['content']['size'] = e['response']['content']['size']
	r['content']['data'] = e['response']['content']['text']
	# timings
	r['timing'] = e['timings']

	return r

def run(options):

	if not options.file:
		sys.exit('No har input file specified. Aborting.')

	har_file = options.file

	try:
		with open(har_file) as har_data_file:
			har_data = json.load(har_data_file)
	except Exception, ee:	
		sys.exit('Error loading har input file... Aborting.')


	if not options.bugs:
		sys.exit('No ghostery bugs input file. Aborting.')

	bugs_file = options.bugs

	try:
		with open(bugs_file) as bugs_data_file:
			bugs_data = json.load(bugs_data_file)
	except Exception, ee:	
		sys.exit('Error loading bugs data... Aborting.')

	transactions = []
	bugs = bugs_data['bugs']
	tags = bugs_data['tags']
	entries = har_data['log']['entries']
	i = 0
	for e in entries:
		i += 1
		#print str(i) + '/' + str(len(entries))
		url = e['request']['url']
		bug = match(url, bugs) 
		if bug:
			info = format(e, bug)
			transactions.append(info)

	#we leave the ghost tags section... 

	output = {}
	output['browser'] = har_data['log']['browser']
	output['exporter'] = har_data['log']['creator']
	output['date_time'] = har_data['log']['pages'][0]['startedDateTime']
	output['data'] = transactions

	return output


if __name__ == '__main__':

	p = OptionParser();
	p.add_option('-f', '--file', action="store", help="har input file")
	p.add_option('-b', '--bugs', action="store", help="ghostery bugs input file")

	options, args = p.parse_args()

	result = run(options)

	print json.dumps(result, indent=2, separators=(',',':'))