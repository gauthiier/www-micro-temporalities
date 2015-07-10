import sys, csv, json, os, re

def emit_header(browser, exporter, data_time):
	str_s = '<div class="agent">'
	str_s += '<b>Date</b>:<br>'
	str_s += data_time + '\n'
	str_s += '<br>\n'	
	str_s += '<b>Browser</b>:<br>'
	str_s += browser['name']+ '-' + browser['version'] + '\n'
	str_s += '<br>\n'
	str_s += '<b>Exporter</b>:<br>'
	str_s += exporter['name']+ '-' + exporter['version'] + '\n'
	str_s += '<br>\n'	
	str_s += '</div>\n' 
	return str_s


def emit_bug(b):

	bug = b['bug']
	str_s = '<div class="bug ' + bug['type'] + '">'

	# bug
	str_s += '<b>Bug</b>'
	str_s += '<br>'
	str_s += '<div class="data">\n'
	str_s += 'type: ' + bug['type'] + '<br>' + 'property: ' + bug['name']
	str_s += '</div>'

	str_s += '<br>'

	# request
	req = b['request']
	str_s += '<b>Request</b>'
	str_s += '<br>'
	str_s += '<div class="data">\n'
	str_s += req['method'] + '<br>' + req['url'] + '<br>' + req['user_agent']
	str_s += '<br>'
	if 'referer' in req:
		str_s += '<br>'
		str_s += 'Ref: ' + req['referer']
		str_s += '<br>'
	str_s += '</div>'

	str_s += '<br>'

	# response
	res = b['response']
	str_s += '<b>Response</b>'
	str_s += '<br>'
	str_s += '<div class="data">\n'
	if 'server_agent' in res:
		str_s += str(res['status']) + '<br>' + str(res['server_ip']) + '<br>' + res['server_agent'] + '<br>'
	else:
		str_s += str(res['status']) + '<br>' + str(res['server_ip']) + '<br>'
	str_s += '</div>'

	str_s += '<br>'

	# content
	c = b['content']
	str_s += '<b>Content</b>'
	str_s += '<br>'
	str_s += '<div class="data">\n'
	str_s += 'mime type: ' + c['mime_type'] + '<br>'
	str_s += 'size: ' + str(c['size']) + '<br>'

	if len(c['data']) > 500:
		str_s += '<div class="code">\n'
		str_s += html_escape(c['data']) + '\n'
		str_s += '</div>\n'

	str_s += '</div>'
	str_s += '</div>'
	return str_s

def html_escape(text):
	html_escape_table = {
	 "&": "&amp;",
	 '"': "&quot;",
	 "'": "&apos;",
	 ">": "&gt;",
	 "<": "&lt;",
	 "[": "&#91",
	 "]": "&#93"
	 }
	return "".join(html_escape_table.get(c,c) for c in text)

if __name__ == '__main__':

	fp = sys.stdin
	try:
		data = json.loads(fp.read())
	except Exception, ee:	
		sys.exit('Error loading data... Aborting.')

	try:
		template = open(os.path.join('.', 'index_template.html'), 'r+');
	except:
		print('error opening template file. aborting...');
		sys.exit(0);		

	content = ""
	content += emit_header(data['browser'], data['exporter'], data['date_time'])

	bugs = data['data']

	for b in bugs:				
		card = "<div class='card'>\n"
		card += emit_bug(b)
		card += "</div>\n"
		content += card

	html = template.read().replace('[[content]]', content);

	print (html).encode("utf-8")