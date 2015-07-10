#!/usr/bin/python2.7
import sys, json
if __name__ == '__main__':
	fp = sys.stdin
	data = json.loads(fp.read())
	print json.dumps(data, indent=2, separators=(',',':'))