import sys, json

if __name__ == '__main__':

	fp = sys.stdin
	try:
		sdata = fp.read()
		data = json.loads(sdata)
	except Exception, ee:	
		sys.exit('Error loading data... Aborting.')

	apps = data['apps']

	result = {}
	result['ads'] = []
	result['trackers'] = []
	result['analytics'] = []
	result['widgets'] = []
	result['privacy'] = []


	hosts = data['firstPartyExceptions']

	for key, info in apps.iteritems():
		if key in hosts:
			urls = []
			for u in hosts[key]:
				if info['cat'] == 'tracker':
					result['trackers'].append(u)
				elif info['cat'] == 'ad':
					result['ads'].append(u)
				elif info['cat'] == 'analytics':
					result['analytics'].append(u)
				elif info['cat'] == 'widget':
					result['widgets'].append(u)
				elif info['cat'] == 'privacy':
					result['privacy'].append(u)

	print json.dumps(result, indent=2, separators=(',',':'))