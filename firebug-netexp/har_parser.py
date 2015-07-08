import sys, json

if __name__ == '__main__':

	fp = sys.stdin
	try:
		sdata = fp.read()
		data = json.loads(sdata)
	except Exception, ee:	
		sys.exit('Error loading data... Aborting.')

	entries = data['log']['entries']
	for e in entries:
		req = e['request']
		print req['url']