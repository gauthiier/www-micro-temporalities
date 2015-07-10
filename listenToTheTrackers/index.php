<?php
$render = "wav";
if (isset($_GET['render']) && !empty($_GET['render']) && in_array($_GET['render'], array("synth", "wav"))) {
    $render = $_GET['render'];
}
?>
<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">

        <title>Listen to the Trackers</title>
        <meta name="description" content="Listen to the Trackers">
        <meta name="author" content="Erik Borra">

        <!--[if lt IE 9]>
        <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
        <![endif]-->
        <script src="https://code.jquery.com/jquery-1.8.2.js"></script>
        <script src="https://jquery-csv.googlecode.com/git/src/jquery.csv.js"></script>
    </head>

    <body>
        <script>
            var tracker_types, tracker_starts, tracker_ends, tracker_starts_tmp, tracker_ends_tmp, render;
            $(document).ready(function () {
                // load tracker data
                function loadTrackerCsv(csv) {
                    $('#permalink').html('<a href="?csv=' + csv + '&render=<?php echo $render; ?>">permalink</a>');
                    $('#volumes').ajaxStart(function () {
                        $(this).html('loading');
                    });
                    url = "https://raw.githubusercontent.com/gauthiier/www-micro-temporalities/master/webpagetest/filtered/" + csv;
                    $.ajax({
                        type: "GET",
                        url: url,
                        dataType: "text",
                        success: function (data) {
                            $('#volumes').html('Trackers volume (<a href="' + url + '" target="_blank">csv</a>):<br>');
                            var data = $.csv.toObjects(data);
                            var datalength = data.length;
                            tracker_types = [];
                            tracker_starts = {};
                            tracker_ends = {};
                            for (var i = 0; i < datalength; i++) {
                                var tracker_type = data[i]['bug_type'];
                                // set up tracker volume information
                                if (tracker_types.indexOf(tracker_type) == -1) {
                                    tracker_types.push(tracker_type);
<?php if ($render == "synth") { ?>
                                        oscillator[tracker_type] = context.createOscillator();
                                        oscillator[tracker_type].start ? oscillator[tracker_type].start(0) : oscillator[tracker_type].noteOn(0)
<?php } ?>
                                    $('#volumes').append("<div id='" + tracker_type + "'>" + tracker_type + ": <span id='" + tracker_type + "_volume'>10</span></div>");
                                }
                                // keep track of which tracker starts when
                                if (!(tracker_type in tracker_starts))
                                    tracker_starts[tracker_type] = [];
                                tracker_starts[tracker_type].push(data[i]['Start Time (ms)']);
                                // keep track of which tracker ends when
                                if (!(tracker_type in tracker_ends))
                                    tracker_ends[tracker_type] = [];
                                tracker_ends[tracker_type].push(data[i]['Start Time (ms)']);
                            }
                            tracker_starts_tmp = jQuery.extend(true, {}, tracker_starts);
                            tracker_ends_tmp = jQuery.extend(true, {}, tracker_ends);
                            // half as way to get global min and max
                            tracker_min = [];
                            tracker_max = [];
                            for (tracker in tracker_starts) {
                                tracker_min.push(Math.min.apply(Math, tracker_starts[tracker]));
                                tracker_max.push(Math.max.apply(Math, tracker_ends[tracker]));
                            }
                            tracker_min = Math.min.apply(Math, tracker_min);
                            tracker_max = Math.max.apply(Math, tracker_max);
                            $('#tracker_min').html(tracker_min);
                            $('#tracker_max').html(tracker_max);
                        }
                    });
                }
                // load tracker on change
                $('#csvs').on('change', function () {
                    loadTrackerCsv(this.value);
                });
                $("input[name=render]").on('change', function () {
                    var checked = $('input[name=render]:checked').val();
                    window.location = $('#permalink a').attr('href').replace(/render=.*/, 'render=' + checked);
                });

                // load selected tracker
                if ($('#csvs').find(":selected").length > 0)
                    loadTrackerCsv($('#csvs').find(":selected").val());
                else
                    // load first tracker on load
                    loadTrackerCsv($("#csvs option:first").val());
            });</script>
        <?php
        if ($render == "wav") {
            ?>
            <script src="js/soundmanagerv297a-20150601/script/soundmanager2.js"></script>
            <script>
                var sounds = {};
                soundManager.setup({
                    url: 'js/soundmanagerv297a-20150601/swf/',
                    onready: function () {
                        sounds['-'] = soundManager.createSound({
                            id: '-',
                            url: 'Sounds/1 - General content 1sec louder.wav'
                        });
                        sounds['analytics'] = soundManager.createSound({
                            id: 'analytics',
                            url: 'Sounds/2 - Analytics 1sec louder.wav'
                        });
                        sounds['widget'] = soundManager.createSound({
                            id: 'widget',
                            url: 'Sounds/3 - Widgets 1sec.wav'
                        });
                        sounds['ad'] = soundManager.createSound({
                            id: 'ad',
                            url: 'Sounds/4 - Ad 1sec.wav'
                        });
                        sounds['tracker'] = soundManager.createSound({
                            id: 'tracker',
                            url: 'Sounds/5 - Tracker 1sec.wav'
                        });
                    },
                    ontimeout: function () {
                        // Hrmm, SM2 could not start. Missing SWF? Flash blocked? Show an error, etc.?
                        console.log('not found');
                    }
                });</script>
            <?php
        } elseif ($render == "synth") {
            ?>
            <script type='text/javascript'>
                /* oscillator */
                var contextClass = (window.AudioContext ||
                        window.webkitAudioContext ||
                        window.mozAudioContext ||
                        window.oAudioContext ||
                        window.msAudioContext);

                var messageDisplayed = false;

                if (contextClass) {
                    // Web Audio API is available.
                    var context = new contextClass();
                    var gainValue = 0.1;
                    var gainNode = context.createGain ? context.createGain() : context.createGainNode();
                    var oscillator = {};
                } else {
                    e.stopImmediatePropagation();
                    if (!messageDisplayed) {
                        $("#generator").css("padding-top", '0').prepend("<p style='padding:20px;font-size:0.8em;'>Sorry, it looks like your browser is not compatible with this particular feature. If possible, please try again with the latest version of Chrome, Safari or Firefox.</p>");
                        $(this).parents(".tuningTable").before("<p style='padding:20px;font-size:0.8em;'>Sorry, it looks like your browser is not compatible with the tone generator. If possible, please try again with the latest version of Chrome, Safari or Firefox.</p>");
                        messageDisplayed = true;
                    }
                }

                var oscs = {sine: 0, square: 1, sawtooth: 2, triangle: 3};

                var oscOn = function (freq, type, tracker) {
                    console.log(freq, type, tracker);
                    //oscillator[tracker] = context.createOscillator();
                    oscillator[tracker].frequency.value = freq;

                    oscillator[tracker].connect(gainNode);
                    gainNode.connect(context.destination);
                    gainNode.gain.value = gainValue;

                    oscillator[tracker].type = 'sine';


                    // oscillator.start(0);
                };
                var sounds = {'-': 50, 'analytics': 250, 'widget': 450, 'ad': 650, 'tracker': 850, 'privacy': 1050};
            </script>
        <?php } ?>
        <script type="text/javascript">
            var setT, startMS;
            function timeCount() {
                var date = new Date(), ms = date - startMS, ss;
                if (ms - 20 > tracker_max) {
                    // reset and stop
                    tracker_starts = jQuery.extend(true, {}, tracker_starts_tmp);
                    tracker_ends = jQuery.extend(true, {}, tracker_ends_tmp);
                    document.getElementById('counter').innerHTML = tracker_max + 'ms';
                    stopCounter();
                } else {
                    document.getElementById('counter').innerHTML = ms + 'ms';
                    for (tracker in tracker_starts) {
<?php if ($render == "wav") { ?>
                            if (tracker_starts[tracker].length > 0 && tracker_starts[tracker][0] >= ms) {
                                var volume = parseInt($("#" + tracker + "_volume").text()) + 1;
                                $("#" + tracker + "_volume").html(volume);
                                if (tracker in sounds) {
                                    sounds[tracker].stop();
                                    sounds[tracker].play();
                                    sounds[tracker].setVolume(volume);
                                }
                                tracker_starts[tracker].shift();
                            }
                            if (tracker_ends[tracker].length > 0 && tracker_ends[tracker][0] <= ms) {
                                var volume = parseInt($("#" + tracker + "_volume").text()) - 1;
                                $("#" + tracker + "_volume").html(volume);
                                if (tracker in sounds) {
                                    sounds[tracker].stop();
                                    sounds[tracker].play();
                                    sounds[tracker].setVolume(volume);
                                }
                                tracker_ends[tracker].shift();
                            }
<?php } elseif ($render == "synth") { ?>
                            if (tracker_starts[tracker].length > 0 && tracker_starts[tracker][0] >= ms) {
                                var volume = parseInt($("#" + tracker + "_volume").text()) + 1;
                                if (volume > 100)
                                    volume = 100;
                                console.log('volume', volume);
                                oscOn(sounds[tracker] + volume, 1, tracker);
                                $("#" + tracker + "_volume").html(volume);
                                tracker_starts[tracker].shift();
                            }
                            if (tracker_ends[tracker].length > 0 && tracker_ends[tracker][0] <= ms) {
                                var volume = parseInt($("#" + tracker + "_volume").text()) - 1;
                                oscOn(sounds[tracker] + volume, 1, tracker);
                                $("#" + tracker + "_volume").html(volume);
                                tracker_ends[tracker].shift();
                            }
                            if (tracker_ends[tracker].length == 0)
                                oscillator[tracker].disconnect()
<?php } ?>
                    }
                    setT = setTimeout(function () {
                        timeCount()
                    }, 1);
                }
            }
            function startCounter() {
                startMS = new Date();
                timeCount();
            }
            function stopCounter() {
                clearTimeout(setT);
            }
        </script>
        <form action="">
            <select id='csvs' name='csvs'>
                <?php
                $file = file_get_contents('https://github.com/gauthiier/www-micro-temporalities/tree/master/webpagetest/filtered');
                if (preg_match_all("/filtered\/(.+?\.csv)\"/", $file, $matches)) {
                    foreach ($matches[1] as $csv) {
                        $name = urldecode(preg_replace("/wpt_\d+_(.+?)_object.*/", "$1", $csv));
                        $names[$name] = $csv;
                    }
                    ksort($names);
                    foreach ($names as $name => $csv) {
                        if (isset($_GET['csv']) && $_GET['csv'] == urldecode($csv))
                            print "<option value='$csv' SELECTED>$name</option>";
                        else
                            print "<option value='$csv'>$name</option>";
                    }
                }
                ?>
            </select>
            <input type='radio' name='render' value='wav'<?php echo ($render == "wav"?" checked":""); ?>>wav</input>
            <input type='radio' name='render' value='synth'<?php echo ($render == "synth"?" checked":""); ?>>synth</input>
            <input type="button" value="Listen to the trackers" onclick="startCounter()">
            <!--<input type="button" value="Stop" onclick="stopCounter()">-->
        </form>
        <br>
        <?php
        if($render == "wav")
            print "Listening to wav. The volume of one of 6 types of .wav files is increased every time a new tracker of that type starts loading. The sound is decreased when the tracker finishes<br>";
        elseif($render == "synth")
            print "Listening to synth. The frequencies of 6 distinct tones are increased every time a new tracker of that type starts loading. The frequency is decreased when the tracker finishes<br>";
        ?>
        <br>
        <span id='permalink'></span><br>
        <br>
        Trackers start at <span id='tracker_min'></span>ms and end at <span id='tracker_max'></span>ms<br><br>
        Replaying microseconds: <span id="counter">0ms</span><br>
        
        <br>
        <div id='volumes'></div>
    </body>
</html>

