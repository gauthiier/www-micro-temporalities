import sys, csv, json, os, re

def emit_header():
	str_s = '<div class="agent">'
	str_s += '<b>Location</b>:<br>'
	str_s += 'Amsterdam<br>\n'
	str_s += '<br>\n'
	str_s += '<b>User-Agent</b>:<br>'
	str_s += "Mozilla/5.0 (Windows NT 6.1; WOW64)<br>AppleWebKit/537.36 (KHTML, like Gecko)<br>Chrome/43.0.2357.132 Safari/537.36 PTST/221\n"
	str_s += '</div>\n' 
	return str_s


def emit_name(name, date, time):
	str_s = '<div class="name">' + name + '</div>\n'
	str_s +=  '<div class="date">' + date + '</div>\n'
	str_s +=  '<div class="time">' + time + ' CEST</div>\n'
	return str_s

def string_format_percentage(pct):
	v = int(pct * 100)
	return str(v)


def emit_table_row(elem, index, total):
	return '<tr>' + '<td>' + index +': ' + '</td><td>'+ str(int(elem[index])) + '</td><td>' + string_format_percentage(elem[index] / total) + '%' + '</td></tr>\n'

def emit_size(size):
	total = size['widget'] + size['ad'] + size['privacy'] + size['-'] + size['analytics'] + size['tracker']
	if total == 0:
		total = 1
	str_s = '<div class="size">'
	str_s += '<h4>Objects Size (bytes)</h4>\n'
	str_s += '<div class="data">\n'
	str_s += '<table>\n'
	str_s += emit_table_row(size, 'ad', total).replace('ad', 'ads')
	str_s += emit_table_row(size, 'analytics', total)
	str_s += emit_table_row(size, 'tracker', total).replace('tracker', 'trackers')
	str_s += emit_table_row(size, 'widget', total).replace('widget', 'widgets')
	str_s += emit_table_row(size, '-', total).replace('-', 'other')
	str_s += '</table>\n'
	str_s += '</div>\n'
	str_s += '</div>\n'
	return str_s

def emit_item(item):
	total = item['total']
	total_junk = item['widget'] + item['ad'] + item['privacy'] + item['analytics'] + item['tracker']
	if total == 0:
		total = 1
	str_s = '<div class="items">'
	str_s += '<h4>Page Http Request Elements</h4>\n'
	str_s += '<div class="data">\n'
	str_s += '<table>\n'	
	str_s += emit_table_row(item, 'ad', total).replace('ad', 'ads')
	str_s += emit_table_row(item, 'analytics', total)
	str_s += emit_table_row(item, 'tracker', total).replace('tracker', 'trackers')
	str_s += emit_table_row(item, 'widget', total).replace('widget', 'widgets')
	str_s += emit_table_row(item, '-', total).replace('-', 'other')
	str_s += '</table>\n'
	str_s += '</div>\n'
	str_s += '</div>\n'
	return str_s

def emit_time(time):
	total = time['widget'] + time['ad'] + time['privacy'] + time['-'] + time['analytics'] + time['tracker']
	if total == 0:
		total = 1
	str_s = '<div class="times">'
	str_s += '<h4>(Micro) Timing (ms)</h4>\n'
	str_s += '<div class="data">\n'
	str_s += '<table>\n'	
	str_s += emit_table_row(time, 'ad', total).replace('ad', 'ads')
	str_s += emit_table_row(time, 'analytics', total)
	str_s += emit_table_row(time, 'tracker', total).replace('tracker', 'trackers')
	str_s += emit_table_row(time, 'widget', total).replace('widget', 'widgets')
	str_s += emit_table_row(time, '-', total).replace('-', 'other')
	str_s += '</table>\n'
	str_s += '</div>\n'
	str_s += '</div>\n'
	return str_s

def parse_nbr(name):
	#wpt_01_[Reddit]_[Amsterdam]_object__filtered
	return  name.split("_")[1]

if __name__ == '__main__':

	fp = sys.stdin
	try:
		stats = json.loads(fp.read())
	except Exception, ee:	
		sys.exit('Error loading data... Aborting.')

	try:
		template = open(os.path.join('.', 'index_template.html'), 'r+');
	except:
		print('error opening template file. aborting...');
		sys.exit(0);		

	content = ""
	content += emit_header()
	for e in stats:				
		card = "<div class='card' onclick=\"window.open('" + e['name'] + ".csv.svg" + "','external');\">\n"
		stats = e['stats']
		card += parse_nbr(e['name']) + '<br>' 
		card += "\t\t\t" + emit_name(stats['host'], stats['date'], stats['time'])		
		card += "\t\t\t" + emit_item(stats['items'])
		card += "\t\t\t" + emit_size(stats['sizes'])
		card += "\t\t\t" + emit_time(stats['times'])
		card += "</div>\n"
		content += card

	html = template.read().replace('[[content]]', content);

	print html
	

