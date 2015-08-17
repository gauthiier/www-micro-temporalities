
var modfactor = 750.0;
var modfactor_gain = 10750.0;

function create_none_synth() {
	var s = new FMSynth('triangle', 100, 'sawtooth', 2, 300);
	s.add_filter(new LowPassFilter());
	s.update = function(val) {
		this.modulator_freq(val / modfactor);
	};
	return s;
}

function create_ad_synth() {
	var s = new SimpleOscillator('square', 100);
	s.add_filter(new NoiseConvolver());
	s.update = function(val) {
		this.modulator_freq(val / 25);
	};	
	return s;
}

function create_tracker_synth() {
	var s = new PinkNoiseGenerator();
	//s.add_filter(new NoiseConvolver());
	s.update = function(val) {
		this.modulator_gain(val / modfactor_gain);
	};	
	return s;
}

function create_analytics_synth() {
	var s = new WhiteNoiseGenerator();
	//s.add_filter(new DistortionShaper(55));
	s.update = function(val) {
		this.modulator_gain(val / modfactor_gain);
	};	
	return s;
}

function create_widget_synth() {
	var s = new PinkNoiseGenerator();
	s.update = function(val) {
		this.modulator_gain(val / modfactor_gain);
	};	
	return s;
}

function create_privacy_synth() {
	var s = new WhiteNoiseGenerator();
	s.update = function(val) {
		this.modulator_gain(val / modfactor_gain);
	};	
	return s;
}
