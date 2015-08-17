var data = [];		
var start_times_dict = {};
var end_times_dict = {};
var start_times = [];
var end_times = [];

var next_start = 0;
var next_end = 0;

var processing_data = [];

// timer parameters
var tick_cnt = 0;   			/// this is passed to the drawing
var time_incr_ms = 2;
var time_end = 0;
var interval_id = 0;

var p = true;

var params = {
	"-" : {'bytes': 0, 'synth': null, 'active': 0},
	"ad" : {'bytes': 0, 'synth': null, 'active': 0},
	"tracker" : {'bytes': 0, 'synth': null, 'active': 0},
	"analytics" : {'bytes': 0, 'synth': null, 'active': 0},
	"widget" : {'bytes': 0, 'synth': null, 'active': 0},
	"privacy" : {'bytes': 0, 'synth': null, 'active': 0}
};

function synthesise(csv_input_file_url) {

	$.ajax({
		type: 'GET',
		url: csv_input_file_url,
		dataType: 'text',
		success: function(resp) {
			data = $.csv.toObjects(resp);		
			start_times = {};
			end_times = {};

			for(var i = 0; i < data.length; i++) {

				var start = +data[i]['Start Time (ms)'];
				var end = +data[i]['End Time (ms)'];
				var size = +data[i]['Object Size'];

				if(!(start in start_times_dict)) {
					start_times_dict[start] = [];	
				} 
				start_times_dict[start].push(i);

				if(!(end in end_times_dict)) {
					end_times_dict[end] = [];	
				} 
				end_times_dict[end].push(i);

				data[i].incr = linear_increment(start, end, size);
				data[i].incr_tick = 0;

				if(end > time_end) time_end = end;
			}

			$('#end').html(time_end);

			start_times = Object.keys(start_times_dict);
			end_times = Object.keys(end_times_dict);

			start_times.sort(function(a, b){
				return a - b;
			});
			end_times.sort(function(a, b) {
				return a - b;
			});

			// create synths

			params['-'].synth = create_none_synth();
			params['ad'].synth = create_ad_synth();
			params['tracker'].synth = create_tracker_synth();
			params['analytics'].synth = create_analytics_synth();
			params['widget'].synth = create_widget_synth();
			params['privacy'].synth = create_privacy_synth();

			stop_all_synths();

			interval_id = window.setInterval(tick, time_incr_ms);

		},
		error: function(xhr, status, error) {
			console.log("error loading -- "  + csv_input_file);
		}
	});	
}

function linear_increment(start_ms, end_ms, size_bytes) {
	return size_bytes / (end_ms - start_ms);
}

function start_all_synths() {
	p = false;
	params['-'].synth.start();
	params['ad'].synth.start();
	params['tracker'].synth.start();
	params['analytics'].synth.start();
	params['widget'].synth.start();
	params['privacy'].synth.start();
}

function stop_all_synths() {
	p = true;
	params['-'].synth.stop();
	params['ad'].synth.stop();
	params['tracker'].synth.stop();
	params['analytics'].synth.stop();
	params['widget'].synth.stop();
	params['privacy'].synth.stop();
}


function tick() {	

	if(p) return;

	$('#time').html(tick_cnt);
	if(tick_cnt >= time_end + 1) {
		window.clearInterval(interval_id);
		stop_all_synths();
	} else if(tick_cnt == 0) {
		start_all_synths();
	}

	if(start_times[next_start] == tick_cnt) {
		var start_indices = start_times_dict[tick_cnt];
		processing_data = processing_data.concat(start_indices)
		for(var i = 0; i < start_indices.length; i++) {
			var d = data[start_indices[i]]
			params[d.bug_type].active = params[d.bug_type].active + 1;
		}
		next_start++;
	}
	if(end_times[next_end] == tick_cnt) {

		var end_indices = end_times_dict[tick_cnt];
		for(var i = 0; i < end_indices.length; i++) {
			var processing_indx = processing_data.indexOf(end_indices[i]);
			if(processing_indx != -1) {
				var d = data[end_indices[i]]
				processing_data.splice(processing_indx, 1);
				params[d.bug_type].bytes -= parseInt(d['Object Size']);
				params[d.bug_type].active = params[d.bug_type].active - 1;
			} else {
				console.log('not proccesed -- ' + end_indices[i]);
			}
		}

		next_end++;
	}

	for(var i = 0; i < processing_data.length; i++) {
		var d = data[processing_data[i]];
		params[d.bug_type].bytes += d.incr;
		d.incr_tick = d.incr_tick + 1;
	}

	params['-'].synth.update(params['-'].bytes);
	params['ad'].synth.update(params['ad'].bytes);
	params['tracker'].synth.update(params['tracker'].bytes);
	params['analytics'].synth.update(params['analytics'].bytes);
	params['widget'].synth.update(params['widget'].bytes);
	params['privacy'].synth.update(params['privacy'].bytes);

	// $('#none').html(params['-'].active);
	// $('#none_bytes').html(Math.ceil(params['-'].bytes));

	// $('#ad').html(params['ad'].active);
	// $('#ad_bytes').html(Math.ceil(params['ad'].bytes));

	// $('#tracker').html(params['tracker'].active);
	// $('#tracker_bytes').html(Math.ceil(params['tracker'].bytes));

	// $('#analytics').html(params['analytics'].active);
	// $('#analytics_bytes').html(Math.ceil(params['analytics'].bytes));

	// $('#widget').html(params['widget'].active);
	// $('#widget_bytes').html(Math.ceil(params['widget'].bytes));

	// $('#privacy').html(params['privacy'].active);
	// $('#privacy_bytes').html(Math.ceil(params['privacy'].bytes));


	tick_cnt++; 

}

