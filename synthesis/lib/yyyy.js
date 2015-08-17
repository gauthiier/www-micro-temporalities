////////////
//////////////////////////// 
////////////

var AudioContext = window.AudioContext || window.webkitAudioContext;

var audioCtx = new AudioContext();

function Modulator(waveform, freq, gain) {
  // actual modulating freq
  this.osc = audioCtx.createOscillator();
  this.osc.type = waveform;
  this.osc.frequency.value = freq;    
  // not sure about this -- but the gain is what modulates
  this.gain = audioCtx.createGain();
  this.gain.gain.value = gain;
  // connect
  this.osc.connect(this.gain);
}

function Carrier(waveform, freq) {
  this.osc = audioCtx.createOscillator();
  this.osc.type = waveform;
  this.osc.frequency.value = freq;    
  this.gain = audioCtx.createGain();
  this.osc.connect(this.gain);
}

function FMSynth(waveform_c, freq_c, waveform_m, freq_m, gain_m) {

	this.carrier = new Carrier(waveform_c, freq_c);
	this.modulator = new Modulator(waveform_m, freq_m, gain_m);

	this.bitcrusher_filter = new BitCrusherFilter();

	this.modulator.gain.connect(this.carrier.osc.frequency);
	this.carrier.gain.connect(audioCtx.destination);

	this.started = false;

	this.start = function() {
		if(!this.started) {
			this.carrier.osc.start(0);
			this.modulator.osc.start(0);
			this.started = true;
		} else {
			this.carrier.gain.gain.value = 1.0;
		}
	}

	this.stop = function() {
		this.carrier.gain.gain.value = 0.0;
	}

	this.modulator_freq_incr = function(incr) {
		this.modulator.osc.frequency.value = this.modulator.osc.frequency.value + incr;
	}

	this.modulator_freq = function(freq) {
		this.modulator.osc.frequency.value = freq;
	}

	this.add_filter = function (filter) {
		this.filter = filter;
		this.carrier.osc.disconnect(this.carrier.gain);
		this.carrier.osc.connect(this.filter);
		this.filter.connect(this.carrier.gain);
	}

}

function SimpleOscillator(waveform, freq) {

	this.oscillator = new Carrier(waveform, freq);
	this.oscillator.gain.connect(audioCtx.destination);

	this.started = false;

	this.start = function() {
		if(!this.started) {
			this.oscillator.osc.start(0);
			this.started = true;
		} else {
			this.oscillator.gain.gain.value = 1.0;
		}
	}

	this.stop = function() {
		this.oscillator.gain.gain.value = 0.0;
	}

	this.modulator_freq_incr = function(incr) {
		this.oscillator.osc.frequency.value = this.modulator.osc.frequency.value + incr;
	}

	this.modulator_freq = function(freq) {
		this.oscillator.osc.frequency.value = freq;
	}

	this.add_filter = function (filter) {
		this.filter = filter;
		this.oscillator.osc.disconnect(this.oscillator.gain);
		this.oscillator.osc.connect(this.filter);
		this.filter.connect(this.oscillator.gain);
	}	


}

function WhiteNoiseGenerator() {

	// generates 2 sec noise buffer 
	var bufferSize = audioCtx.sampleRate * 2;
	var noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
	var out = noiseBuffer.getChannelData(0);
	for(var i = 0; i < bufferSize; i++) {
		out[i] = Math.random() * 2 - 1;
	}

	this.whitenoise = audioCtx.createBufferSource();
	this.whitenoise.buffer = noiseBuffer;
	this.whitenoise.loop = true;

	this.gain = audioCtx.createGain();
  	this.whitenoise.connect(this.gain);
  	this.gain.connect(audioCtx.destination);

  	this.started = false;

  	this.start = function() {
  		if(!this.started)
  			this.whitenoise.start(0);
  		this.started = true;
  	}	

	this.stop = function() {
		this.gain.gain.value = 0.0;
		this.started = false;
	}

	this.modulator_gain_incr = function(incr) {
		this.gain.gain.value = this.gain.gain.value + incr;
	}

	this.modulator_gain = function(gain) {
		this.gain.gain.value = gain;
	}

	this.add_filter = function(filter) {
		this.filter = filter;
		this.whitenoise.disconnect(this.gain);
		this.whitenoise.connect(this.filter);
		this.filter.connect(this.gain);
	}

}

function PinkNoiseGenerator() {

	var bufferSize = 4096;
	this.pinknoise = audioCtx.createScriptProcessor(bufferSize, 1, 1);
	var b0, b1, b2, b3, b4, b5, b6;
    b0 = b1 = b2 = b3 = b4 = b5 = b6 = 0.0;
	this.pinknoise.onaudioprocess = function(e) {
		var out = e.outputBuffer.getChannelData(0);
		for(var i = 0; i < bufferSize; i++) {
			var white = Math.random() * 2 - 1;
            b0 = 0.99886 * b0 + white * 0.0555179;
            b1 = 0.99332 * b1 + white * 0.0750759;
            b2 = 0.96900 * b2 + white * 0.1538520;
            b3 = 0.86650 * b3 + white * 0.3104856;
            b4 = 0.55000 * b4 + white * 0.5329522;
            b5 = -0.7616 * b5 - white * 0.0168980;
            out[i] = b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362;
            out[i] *= 0.11; // (roughly) compensate for gain
            b6 = white * 0.115926;			
		}
	};
	
	this.gain = audioCtx.createGain();
	this.pinknoise.connect(this.gain);
  	this.gain.connect(audioCtx.destination);

  	this.started = false;

  	this.start = function() {
  	}	

	this.stop = function() {
		this.gain.gain.value = 0.0;
		this.started = false;
	}

	this.modulator_gain_incr = function(incr) {
		this.gain.gain.value = this.gain.gain.value + incr;
	}

	this.modulator_gain = function(gain) {
		this.gain.gain.value = gain;
	}

	this.add_filter = function(filter) {
		this.filter = filter;
		this.pinknoise.disconnect(this.gain);
		this.pinknoise.connect(this.filter);
		this.filter.connect(this.gain);
	}	

}

//////////// Filters

function BitCrusherFilter() {
	var bufferSize = 4096;
	var node = audioCtx.createScriptProcessor(bufferSize, 1, 1);
	node.bits = 14; // between 1 and 16
    node.normfreq = 0.1; // between 0.0 and 1.0
    var step = Math.pow(1/2, node.bits);
    var phaser = 0;
    var last = 0;
    node.onaudioprocess = function(e) {
        var input = e.inputBuffer.getChannelData(0);
        var output = e.outputBuffer.getChannelData(0);
        for (var i = 0; i < bufferSize; i++) {
            phaser += node.normfreq;
            if (phaser >= 1.0) {
                phaser -= 1.0;
                last = step * Math.floor(input[i] / step + 0.5);
            }
            output[i] = last;
        }
    };
    return node;
}

function LowPassFilter() {
	var bufferSize = 4096;
	var node = audioCtx.createScriptProcessor(bufferSize, 1, 1);
	var prev = 0;
	node.onaudioprocess = function(e) {
		var input = e.inputBuffer.getChannelData(0);
		var out = e.outputBuffer.getChannelData(0);
		for (var i = 0; i < bufferSize; i++) {
			out[i] = (input[i] + prev) / 2.0;
			prev = out[i]; 
		}
	};
	return node;
}

//////////// Convolvers

function NoiseConvolver() {
	var convolver = audioCtx.createConvolver();
	var noiseBuffer = audioCtx.createBuffer(2, 0.5 * audioCtx.sampleRate, audioCtx.sampleRate);
	var left = noiseBuffer.getChannelData(0);
	var rigth = noiseBuffer.getChannelData(1);
	for(var i = 0; i < noiseBuffer.length; i++) {
		left[i] = Math.random() * 2 - 1;
		rigth[i] = Math.random() * 2 - 1;
	}
	convolver.buffer = noiseBuffer;
	return convolver;
}

//////////// WaveShapers

function DistortionShaper(distortion_val) {
	this.waveshaper = audioCtx.createWaveShaper();	

	this.makeDistortionCurve = function(amount) {
	  var k = typeof amount === 'number' ? amount : 50,
	    n_samples = 44100,
	    curve = new Float32Array(n_samples),
	    deg = Math.PI / 180,
	    i = 0,
	    x;
	  for ( ; i < n_samples; ++i ) {
	    x = i * 2 / n_samples - 1;
	    curve[i] = ( 3 + k ) * x * 20 * deg / ( Math.PI + k * Math.abs(x) );
	  }
	  return curve;
	}

	this.distortion = function(amount) {
		this.waveshaper.curve = this.makeDistortionCurve(amount);		
	}

	this.waveshaper.curve = this.makeDistortionCurve(distortion_val);

	return this.waveshaper;
}










