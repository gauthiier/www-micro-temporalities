var refresh_rate_ms = 4;
var bb;

function draw(url) {

	if(/csv$/.test(url)) {
		url = url + '.svg';
	} else {
		return;
	}

	d3.xml(url, function(xml) {
		svg_node = document.importNode(xml.documentElement, true);
		svg = d3.select('#track');
		svg.style('width', svg_node.width.baseVal.value);
		svg.style('height', svg_node.height.baseVal.value);
		svg.node().appendChild(svg_node);

		d3.select(svg_node)
			.attr('id', 'svg_track');

			// <input type="button" value="wwwwwwaaavves" onclick="start('wpt_05_[NY Times]_[Amsterdam]_object__filtered.csv')">
		var g = d3.select(svg_node).append('g');
		var b = g.append('foreignObject')
			.attr('x', '85')
			.attr('y', '350')
			.attr('width', '100')
			.attr('height', '100')		
			.append('xhtml:body');
		bb = b.append('input')
			.attr('type', 'button')
			.attr('value', 'synthesise')
			.attr('onclick', 'go()');

		var line = svg.append('svg:line')
			.attr('x1', 0)
			.attr('y1', 0)
			.attr('x2', 0)
			.attr('y1', svg_node.height.baseVal.value)
			.style('stroke', 'rgb(255,0,0)')
			.style('stroke-width', 1);

		window.setInterval( function() {
			line.attr('x1', tick_cnt);	//var tick_cnt = 0;  // from ssss.js
			line.attr('x2', tick_cnt);
		}, refresh_rate_ms);

	});
}

function go() {
	if(bb.attr('value') == 'pause') {
		bb.attr('value', 'synthesise');
		stop_all_synths();
	} else {
		bb.attr('value', 'pause');
		start_all_synths();
	}
}

