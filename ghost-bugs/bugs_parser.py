import sys, json

def reorder_ids(bugs):
	result = {}
	for key, info in bugs.iteritems():
		id = info['aid']
		result[str(id)] = key
	return result


if __name__ == '__main__':

	fp = sys.stdin
	try:
		sdata = fp.read()
		data = json.loads(sdata)
	except Exception, ee:	
		sys.exit('Error loading data... Aborting.')

	apps = data['apps']
	bugs = reorder_ids(data['bugs'])

	result = {}
	result['ads'] = []
	result['trackers'] = []
	result['analytics'] = []
	result['widgets'] = []
	result['privacy'] = []

	hosts = data['firstPartyExceptions']

	for key, info in apps.iteritems():
		k = bugs[key] 
		if k in hosts:
			urls = []
			for u in hosts[k]:
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