/**
    This code from OSF repository https://osf.io/jmz79/ accompanies the publication "Online webcam-based eye tracking in cognitive science: a first look" by Semmelmann & Weigelt, published in Behavior Research Methods in 2017. Please find the abstract and information about the code, analyses, and data below. This work is intended for scientific use only.
    Written by Kilian Semmelmann, tolcam@ksemmelm.de, 2017
**/

/************************************
 * HELPER FUNCTIONS
 ************************************/
/**
 * Shuffles array in place.
 * @param {Array} a items The array containing the items.
 * @author http://stackoverflow.com/a/2450976/4175553
 */
function shuffle(array) {
    var currentIndex = array.length, temporaryValue, randomIndex;

    // While there remain elements to shuffle...
    while (0 !== currentIndex) {

        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;

        // And swap it with the current element.
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
    }

    return array;
}

/************************************
 * WEBCAM PARAMETERS
 ************************************/
var cam = {};
cam.overlay = '';
cam.width = 400;
cam.height = 300;
cam.topDist = '0px';
cam.leftDist = '0px';
cam.recording = 0;
cam.validating = 0;
cam.calibrating = 0;
cam.initialized = 0;

/************************************
 * CALIBRATION PARAMETERS
 ************************************/
var calibrating = 0;
var t_calibration_start;
var calibration_no = 0;
var calibration = {};
calibration.points = [];
calibration.method = "watch"; // click or watch
calibration.calibrations = 26; // how many calibration dots
calibration.duration = 20; // how often does one position get sampled
calibration.instruction = 'Please fixate the dot<br />that will appear. <br /><br />Do not move your head,<br />only use your eyes.';
calibration.instruction_duration = 5000;

/************************************
 * VALIDATION PARAMETERS
 ************************************/
var validating = 0;
var validation_no = 0;
var validation_current = {"x": 0, "y": 0};
var validation_attempt = 1;
var validation = {};
validation.validations = 5;
validation.duration = 20;
validation.points = [];
validation.timeout = 20000; // if no validation happens within X ms, validation will be ended and re-calibrated
validation.attempts = 25; // how often can validation be failed PER validation
validation.distance = 800; // offset distance in pixel to be a valid validation sample


/************************************
 * DESIGN
 ************************************/
var design = {};
var block_no = 0;
var trial_no = 0;
design.blocks = [
    {'type': 'pursuit', 'trials': 24, 'iti': 500, 'instruction': 'A black dot will appear. Please <br />look at it. When it turns <span style="color: #dd494b;">red</span>,<br /> Please follow its movement with your eyes.<br /><br />Do not move your head, <br />only use your eyes.', 'instruction_duration': 7000}
];
design.blocks = shuffle(design.blocks);
design.blocks_randomized = 1; // shall the blocks be shuffled?
design.trials_randomized = 1; // same for trials
design.calibrate = "high";
design.recalibrate = 1;



/************************************
 * DATA VARIABLES
 ************************************/
var data = [];
var data_current = {};
var status = '-';

/**
data.design = jQuery.extend(true, {}, design);
 **/

/************************************
 * SET UP WEBGAZER
 ************************************/
function loadWebgazer() {
    $('canvas').remove();
    cam.initialized = 0;
    $.getScript( "js/webgazer.js" )
        .done(function( script, textStatus ) {
            initializeWebgazer();
            $('#message').html('Please allow for access on your Webcam on the top part of the screen. <br /><br />Remember: We will NOT transmit your video, but only process it locally and transmit numbers to our server.').show();
        })
        .fail(function( jqxhr, settings, exception ) {
            $( "div.log" ).text( "Triggered ajaxError handler." );
        });
}


function initializeWebgazer() {
    webgazer.clearData()
        .setRegression('ridge') /* currently must set regression and tracker */
        .setTracker('clmtrackr')
        .setGazeListener(function(d, clock) {
            //console.log(data); /* data is an object containing an x and y key which are the x and y prediction coordinates (no bounds limiting) */
            //console.log(clock); /* elapsed time in milliseconds since webgazer.begin() was called */
            if (d !== null) {

                if (cam.calibrating == 1) {
                    var $cd = $('#calibration_dot');
                    var cx = parseInt(Math.round($cd.offset().left));
                    var cy = parseInt(Math.round($cd.offset().top));
                    var cp = d;
                    var dist = Math.sqrt(((cp.x - cx) * (cp.x - cx)) + ((cp.y - cy) * (cp.y - cy)));
                    var c = $('#calibration_cnt').html();
                    data_current.raw.push({'time': clock, 'x': cp.x, 'y': cp.y, 'cx': cx, 'cy': cy, 'dist': dist, 'c': c});
                }


                if (cam.validating == 1) {
                    // see whether dx and dy are within 100px radius of target
                    var dist = parseInt(Math.sqrt(((d.x - validation_current.x) * (d.x - validation_current.x)) + ((d.y - validation_current.y) * (d.y - validation_current.y))));
                    var c = parseInt($('#calibration_cnt').html());
                    if (dist < validation.distance) {
                        data_current.raw.push({'time': clock, 'x': d.x, 'y': d.y, 'vx': validation_current.x, 'vy': validation_current.y, 'dist': dist, 'c': c, 'valid': 1});
                        if (c < calibration.duration) {
                            $('#calibration_cnt').html(++c);
                        } else {
                            cam.validating = 0;
                            clearTimeout(t);
                            $('#calibration_dot').hide();
                            validation_no++;
                            saveData();
                            setTimeout("validate();", 500);
                        }
                    } else {
                        data_current.raw.push({'time': clock, 'x': d.x, 'y': d.y, 'vx': validation_current.x, 'vy': validation_current.y, 'dist': dist, 'c': c, 'valid': 0});
                    }
                }

                if (cam.recording == 1) {
                    var tx = -1;
                    var ty = -1;
                    if (data_current.task == "simple" || data_current.task == "pursuit") {
						console.log('gaze: '+d)
                        var $sd = $('#stimuli_dot');
                        var tx = parseInt(Math.round($sd.offset().left));
                        var ty = parseInt(Math.round($sd.offset().top));
                    }
                    data_current.raw.push({'time': clock, 'x': d.x, 'y': d.y, 'tx': tx, 'ty': ty, 'status': status});
                    //console.log(data.trials[trial_no].raw.length + ' ' + d.x + ' ' + d.y);
                }
            }
        })
        .begin()
        .showPredictionPoints(false); /* shows a square every 100 milliseconds where current prediction is */

    cl = webgazer.getTracker().clm;

    checkWebgazer();
}


function checkWebgazer() {
    if (webgazer.isReady()) {
        console.log('webgazer is ready.');
        initializeCam();
    } else {
        setTimeout(checkWebgazer, 100);
    }
}

/************************************
 * SET UP WEBCAM
 ************************************/
function initializeCam() {
    var video = document.getElementById('webgazerVideoFeed');
    video.style.display = 'block'; // block
    video.style.position = 'relative';
    video.width = cam.width;
    video.height = cam.height;
    video.style.margin = '0px';
    $('#webgazerVideoFeed').css({
        'left': '50%',
        'transform': 'translate(-50%, 0)',
        'margin': '20px'
    }).detach().insertAfter('#webcam_insert').get(0).play();

    webgazer.params.imgWidth = cam.width;
    webgazer.params.imgHeight = cam.height;

    cam.overlay = document.getElementById('overlay');
    if (cam.overlay === null) {
        cam.overlay = document.createElement('canvas');
        cam.overlay.id = 'overlay';
        document.body.appendChild(cam.overlay);
    }
    cam.overlay.style.position = 'absolute';
    cam.overlay.width = cam.width;
    cam.overlay.height = cam.height;
    cam.overlay.style.top = cam.topDist;
    cam.overlay.style.left = cam.leftDist;
    cam.overlay.style.margin = '0px';

    cam.initialized = 1;

    $('#message').html('Webcam access successful.').delay(1000).fadeOut(1000);
}

/************************************
 * START BLOCKS
 ************************************/
function prepareBlock() {
    if (cam.initialized == 1) {
        if (block_no < design.blocks.length) {
            trial_no = 0;

            webgazer.resume();
            if (design.recalibrate == 1 || block_no == 0) {
                $('#instruction_message').html(calibration.instruction).show();
                setTimeout("$('#instruction_message').fadeOut(1000);", calibration.instruction_duration);
                setTimeout("startCalibration();", design.blocks[block_no].instruction_duration + 2000);
            } else {
                $('#instruction_message').html(design.blocks[block_no].instruction).show();
                setTimeout("$('#instruction_message').fadeOut(1000);", design.blocks[block_no].instruction_duration);
                setTimeout("prepareTrial();", design.blocks[block_no].instruction_duration + 2000);
            }
        } else {
            endExperiment();
        }
    } else {
        setTimeout("prepareBlock();", 500);
    }
}


/************************************
 * CALIBRATE
 ************************************/
function startCalibration() {
    $('.stimuli').hide();
    $('#calibration_dot').hide();
    if (block_no == 0) {
        $('#calibration_dot').click(function() {
            calibrateHit();
        });
    }
    calibration_no = 0;
    webgazer.clearData();
    window.localStorage.clear();
    //webgazer.begin();
    t_calibration_start = new Date().getTime();
    calibrate();
}

function calibrate() {
    clearTimeout(t);
    if (calibration_no < calibration.calibrations) {
        $('#calibration_cnt').html(calibration.duration);
        $c = $('#calibration_dot');
        //var c = Math.floor(Math.random() * calibration.points.length);
        //var p = calibration.points.splice(c, 1)[0];
        if (calibration.points.length == 0) {
            calibration.points = shuffle([
                {x: "20%", y: "20%"},
                {x: "50%", y: "20%"},
                {x: "80%", y: "20%"},
                {x: "20%", y: "50%"},
            ]);
        }
        var p = calibration.points.pop();
        $c.css({
            'left' : p.x,
            'top' : p.y
        });

        data_current = {
            'type': 'calibration',
            'block': block_no,
            'trial': calibration_no,
            'x': p.x,
            'y': p.y,
            'raw': []
        };

        cam.calibrating = 1;
        $c.show();
        if (calibration.method == 'watch') {
            t = setTimeout("autoCalibration();", 750);
        }
    } else {
        endCalibration();
    }
}

function calibrateHit() {
    var c = $('#calibration_cnt').html();
    /*
    if ($('#webgazerVideoFeed').css('display') == 'block') {
        $('#webgazerVideoFeed').css({
            top: cam.topDist,
            left: cam.leftDist,
            display: 'none',
            transform: '0'
        });
    }*/
    if (c > 1 && cam.calibrating == 1) {
        $('#calibration_cnt').html(--c);
        if (calibration.method == "watch") {
            t = setTimeout("autoCalibration();", 100);
            //requestAnimationFrame(autoCalibration);
        }
    } else {
        $('#calibration_cnt').html(9999);
        clearTimeout(t);
        cam.calibrating = 0;
        $('#calibration_dot').hide();
        calibration_no++;
        saveData();
        calibrate();
    }
    return false;
}

var t;
function autoCalibration() {
    calibrateLog();
    if (cam.calibrating == 1) {
        calibrateHit();
    }
}

function calibrateLog() {
    var $cd = $('#calibration_dot');
    var cx = parseInt(Math.round($cd.offset().left));
    var cy = parseInt(Math.round($cd.offset().top));
    webgazer.watchListener(cx, cy);
}


function endCalibration() {
    clearTimeout(t);
    $('#calibration_dot').unbind("click");
    startValidation();
}



/************************************
 * VALIDATE
 ************************************/
function startValidation() {
    validation_no = 0;
    validate();
}

function validate() {
    clearTimeout(t);
    if (validation_no < validation.validations) { // if we there are validations left
        $('#calibration_cnt').html(0);
        var $c = $('#calibration_dot');
        if (validation.points.length == 0) {
            validation.points = shuffle([
                {x: "20%", y: "20%"},
                {x: "80%", y: "20%"},
                {x: "50%", y: "50%"},
                {x: "20%", y: "80%"},
                {x: "80%", y: "80%"}
                                        ]);
        }
        var vp = validation.points.pop();
        $c.css({
            'left' : vp.x,
            'top' : vp.y
        });
        $c.show();
        validation_current.x = Math.round($c.offset().left);
        validation_current.y = Math.round($c.offset().top);

        data_current = {
            'type': 'validation',
            'block': block_no,
            'trial': validation_no,
            'x': validation_current.x,
            'y': validation_current.y,
            'raw': []
        };
        cam.validating = 1;
        t = setTimeout("validateFail();", validation.timeout);
//t = setTimeout('validation = 0;', 3000);
    } else {
        endValidation();
    }
}

function validateFail() {
    data_current.type = 'validationfail';
    data_current.attempt = validation_attempt;
    saveData();


    cam.validating = 0;
    webgazer.pause();

    $('.stimuli').hide();
    if (validation_attempt >= validation.attempts) {
        $('#message').html('Unforuntately, the calibration failed too many times. Therefore, you can not participate in this study. Please contact <a href="mailto:kilian.semmelmann@rub.de">kilian.semmelmann@rub.de</a> if you have any questions. Thanks for your interest.').show();
    } else {
        validation_attempt++;
        $('#message').html('The calibration failed. <br />Please follow the instructions and try again (try ' + (validation_attempt) + ' of ' + validation.attempts + ').').show().delay(5000).fadeOut(1000);
        $('#instruction').show();
    }
    // TOOD: log validation-fail
}

function endValidation() {
    cam.validating = 0
    validation_attempt = 1;
    webgazer.pause();
    $('#instruction_message').html(design.blocks[block_no].instruction).show();
    setTimeout("$('#instruction_message').fadeOut(1000);", design.blocks[block_no].instruction_duration);
    setTimeout("prepareTrial();", design.blocks[block_no].instruction_duration + 2000);
}



/************************************
 * START EXPERIMENT
 ************************************/
var t_trial_start;
function prepareTrial() {
    status = "prepare";
    $('.stimuli').hide();
    data_current = {
        'type': 'trial',
        'block': block_no,
        'trial': trial_no,
        'raw': []
    };
    webgazer.resume();
    startTrial();
}


function startTrial() {
    t_trial_start = new Date().getTime();
    $('#stimuli_fixation').show();
    status = "fixation_onset";
    // use start function of block-type name
    var fn = design.blocks[block_no].type+"Start";
    window[fn]();
}


var heat;
function endTrial() {
    clearTimeout(t);
    cam.recording = 0;
    webgazer.pause();
    status = "end";
    $('.stimuli').hide();
    trial_no++;
    saveData();

    if (trial_no < design.blocks[block_no].trials) {
		console.log('prepare trial')
        setTimeout("prepareTrial();", design.blocks[block_no].iti);
    } else {
        block_no++;
        if (block_no < design.blocks.length) {
            window.localStorage.clear();
            webgazer.clearData();
            //loadWebgazer();
            //prepareBlock();
            navigation('pause');
        } else {
            endExperiment();
        }
    }
}


function saveData() {
	console.log('save data' + data_current)
    data.push(data_current);
    data_current = {};
    sendData();
}

function sendData() {
    if (data.length > 0) {
        var d = data.shift();
        $.ajax({
            url : "process.php",
            type: "POST",
            data : {'action': 'save', 'type': d.type, 'data': d},
            tryCount : 0,
            retryLimit : 10,
            success: function(resp, textStatus, jqXHR) {
                console.log(resp);
                if (data.length > 0) {
                    sendData();
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                //$('#message').html('uh-oh.').fadeIn(500).delay(1000).fadeOut(500); // TODO
                this.tryCount++;
                if (this.tryCount <= this.retryLimit) {
                    //try again
                    $.ajax(this);
                    return;
                }
                console.log(jqXHR);
            }
        });
    }
}


function endExperiment() {
    webgazer.clearData().end();
    $('#instruction').show();
    page++;
    navigation('continue');
    $.ajax({
        type: "POST",
        url: "endmail.php",
        data: {
            wat: 'wat'
        }
    });
    //heatmap();
}


/************************************
 * SIMPLE DOT VIEWING PARADIGM
 * If you want to introduce your own paradigms, follow the same structure and extend the design array above.
 ************************************/
var tSimple = {};
tSimple.positions = [];
function simpleStart() {
    // if we don't have dot-positions any more, refill the array
    if (tSimple.positions.length == 0) {
        tSimple.positions = shuffle([
            {x: "20%", y: "20%"},
            {x: "50%", y: "20%"},
            {x: "80%", y: "20%"},
            {x: "20%", y: "50%"},
            {x: "80%", y: "50%"},
            {x: "20%", y: "80%"},
            {x: "50%", y: "80%"},
            {x: "80%", y: "80%"}
        ]);
    }
    var pos = tSimple.positions.pop();
    $('#stimuli_dot').css({
        'top': pos.y,
        'left': pos.x
    });
    data_current.task = 'simple';
    data_current.x = pos.x;
    data_current.y = pos.y;
    data_current.condition = 'dot_' + pos.x + '_' + pos.y;

    cam.recording = 1;
    setTimeout('$("#stimuli_fixation").hide(); status = "fixation_offset";', 1500);
    setTimeout('simpleShowdot();', 2000);
}

function simpleShowdot() {
    status = "stimulus_onset";
    $("#stimuli_dot").show();
    setTimeout('status = "stimulus_offset"; endTrial();',  2000);
}


/************************************
 * POSNER VIEWING PARADIGM
 ************************************/
function posnerStart() {
    var p = Math.random() >= 0.5 ? '&gt;&gt;&gt;' : '&lt;&lt;&lt;';
    $('#stimuli_prime').html(p);

    var t = Math.random() >= 0.5 ? 'X' : 'N';
    $('#stimuli_target').html(t);

    var cond = Math.random() >= 0.7 ? 'incongruent' : 'congruent';

    var tpos = 'left';
    if ((cond == 'incongruent' && p == '&lt;&lt;&lt;') || ((cond == 'congruent' && p == '&gt;&gt;&gt;'))) {
        tpos = 'right';
    }

    var pos = {};
    if (tpos == 'left') {
        pos.x = '20%';
        pos.y = '30%';
    } else {
        pos.x = '80%';
        pos.y = '30%';
    }


    $('#stimuli_target').css({
        'top': pos.x,
        'left': pos.y
    });


    data_current.task = 'posner';
    data_current.x = pos.x;
    data_current.y = pos.y;
    data_current.condition = 'posner_' + pos.x + '_' + pos.y + '_' + tpos;

    cam.recording = 1;
    setTimeout("$('#stimuli_fixation').hide();", 1000);
    setTimeout('posnerShowprime();', 1500);
}

function posnerShowprime() {
    $('#stimuli_prime').show();
    setTimeout("posnerShowTarget();", 300);
}

function posnerShowTarget() {
    $('#stimuli_prime').hide();
    $('#stimuli_target').show();
    setTimeout("endTrial();", 1500);
}


/************************************
 * SMOOTH PURSUIT PARADIGM
 ************************************/
var tPursuit = {};
function pursuitStart() {
    $('#stimuli_fixation').hide();
    var pos_possible = shuffle([
        {x: "20%", y: "20%", tx: "80%", ty: "20%"},
        {x: "20%", y: "20%", tx: "20%", ty: "80%"},
        {x: "20%", y: "20%", tx: "80%", ty: "80%"},

        {x: "80%", y: "20%", tx: "20%", ty: "20%"},
        {x: "80%", y: "20%", tx: "20%", ty: "80%"},
        {x: "80%", y: "20%", tx: "80%", ty: "80%"},

        {x: "20%", y: "80%", tx: "20%", ty: "20%"},
        {x: "20%", y: "80%", tx: "80%", ty: "20%"},
        {x: "20%", y: "80%", tx: "80%", ty: "80%"},

        {x: "80%", y: "80%", tx: "20%", ty: "20%"},
        {x: "80%", y: "80%", tx: "80%", ty: "20%"},
        {x: "80%", y: "80%", tx: "20%", ty: "80%"}
    ]);
    var pos = pos_possible[0];
    $s = $('#stimuli_dot');
    $s.css({
        'top': pos.y,
        'left': pos.x
    });

    $s.css({
        'background-color': '#000'
    });


    data_current.task = 'pursuit';
    data_current.x = pos.x;
    data_current.y = pos.y;
    data_current.condition = 'pursuit_' + pos.x + '_' + pos.y + '_' + pos.tx + '_' + pos.ty;

    cam.recording = 1;
    $s.show();
    setTimeout(function() {
        status = "pursuit_start";
        $('#stimuli_dot').css({
            'background-color': '#dd494b'
        }).animate({ "left": pos.tx, "top": pos.ty },
            2000,
            'linear',
        function() {
            status = "pursuit_end";
            setTimeout("endTrial();", 500);
        });
    }, 1500);
}



/************************************
 * FREE VIEWING PARADIGM
 ************************************/
var tFreeview = {};
tFreeview.stimuli = [];
function freeviewStart() {
    if (tFreeview.stimuli.length == 0) {
        for (var k = 1; k <= 30; k++) {
            if (k < 10) {
                tFreeview.stimuli.push("stimuli/tolcam_face_0" + k + ".png");
            } else {
                tFreeview.stimuli.push("stimuli/tolcam_face_" + k + ".png");
            }
        }
        tFreeview.stimuli = shuffle(tFreeview.stimuli);
    }
    var img = tFreeview.stimuli.pop();
    $('#stimuli_fixation').css({
        'top': '50%',
        'left': '50%'
    });
    var type = Math.random() >= 0.5 ? "left" : "right";

    $('#stimuli_img').css({
        "left": type == "left" ? "25%" : "75%",
        "width": "50%",
        "background-image": "url("+img+")"
    });


    data_current.task = 'freeviewing';
    data_current.x = $('#stimuli_img').css('left');
    data_current.y = "0%";
    data_current.condition = 'view_' + img + '_' + type;


    cam.recording = 1;
    setTimeout("$('#stimuli_fixation').hide(); status = 'fixation_offset';", 1000);
    setTimeout("freeviewShow();", 1500);
}

function freeviewShow() {
    status = 'stimulus_onset';
    $('#stimuli_img').show();
    setTimeout("status = 'stimulus_offset'; endTrial();", 3000);
}



/************************************
 * GENERATE AND SHOW HEATMAP
 ************************************/
function heatmap(data) {
    // preprocess data for heatmap
    var bins = []; // create bins and fill them
    for (var y = 0; y < window.innerHeight; y++) {
        for (var x = 0; x < window.innerWidth; x++) {
            bins.push([x, y, 0]);
        }
    }
    // sort fixations into bins and get max
    var max = 0;
    for (var i = 0; i < data[data.length - 1].raw.length; i++) {
        var d = data[data.length - 1].raw[i];
        var dx = Math.round(d.x);
        var dy = Math.round(d.y);
        var pos = (dy * window.innerWidth) + dx;
        if (pos <= bins.length && pos >= 0) {
            bins[pos][2] += 1;
            if (bins[pos][2] > max) {
                max = bins[pos][2];
            }
        } else {
            console.log('dropped ' + pos);
        }
    }

    // remove empty bins
    var binsc = [];
    for (var i = 0; i < bins.length; i++) {
        if (bins[i][2] != 0) {
            binsc.push(bins[i]);
        }
    }

    // create heatmap
    $('body').append("<canvas id=\"heatmap\"></canvas>");
    $('#heatmap').attr('width', window.innerWidth);
    $('#heatmap').attr('height', window.innerHeight);
    heat = simpleheat('heatmap');
    heat.resize();
    heat.radius(30,50);
    heat.max(max).data(binsc).draw();

    $('#stimuli_img').show();
}



function takePhoto(agree) {
    if (agree == 'yes') {
        var canvas = document.getElementById('webgazerVideoCanvas');
        var data_out = canvas.toDataURL("image/jpeg");
        $.ajax({
            type: "POST",
            url: "photo.php",
            data: {
                imgBase64: data_out
            }
        });
    }
    $('#beforetherest').fadeOut(500, function() {
        $('#therest').fadeIn(500);
    });
}


function sendEmail() {
    $.ajax({
        type: "POST",
        url: "sendemail.php",
        data: {
            content: $('#emailtext').val()
        }
    }).success(function (e) {
        $('#message').html('Message sent.').fadeIn(500).delay(1000).fadeOut(1000);
        $('#emailtext').val("");
    }).error(function (e) {
        $('#message').html('ERROR: Message could not be sent.').fadeIn(500).delay(1000).fadeOut(1000);
    });

}


/**
 * navigation
 */
var page = 1;
var oldpage = -1;
var d_consent = undefined;
function navigation(direction) {
    $('#message').hide();

    $('#instruction_continue_text').html("&gt;");


    if (page == 2 && direction == 'continue') {
        if ($("#consent_y").prop("checked")) {
            $("input[name='consent']").checkboxradio('disable');
            $("input[name='consent']").checkboxradio('refresh');
            d_consent = new Date();
            page++;
        } else {
            $('#message').html('Please accept the consent form before continuing.').fadeIn(500).delay(1500).fadeOut(500);
        }
    } else if (page == 3 && direction == 'continue') {
        // save demographics and some information about browser, ua, etc
        var d_birthday = $('#f_birthday').val();
        var d_gender = $('#f_gender').val();
        var d_visual = $('#f_visual').val();

        var d_ident = "-";
        var ss = window.location.hash.substring(1);
        if (ss == "cf") { // crowdflower-reference
            d_ident = $('#f_crowdflowerid').val() != "" ? ("cf_" + $('#f_crowdflowerid').val()) : "cf-";
        } else if (ss == "rub") {
            d_ident = $('#f_rubid').val() != "" ? ("rub_" + $('#f_rubid').val()) : "rub-";
		} else {
            d_ident = $('#f_asd').val() != "" ? ("asd_" + $('#f_asd').val()) : "asd-";
			if (d_ident == "asd_autism" || d_ident == "asd_aspergers" || d_ident == "asd_other") {
				design.blocks = [
                    {'type': 'freeview', 'trials': 15, 'iti': 500, 'instruction': 'Please look at the cross.<br />An image will follow. You are free <br />to look at the image.<br /><br />Do not move your head, <br />only use your eyes.', 'instruction_duration': 5000},
                    {'type': 'freeview', 'trials': 15, 'iti': 500, 'instruction': 'Please look at the cross.<br />An image will follow. You are free <br />to look at the image.<br /><br />Do not move your head, <br />only use your eyes.', 'instruction_duration': 5000}
				];
				console.log(design.blocks);
			}
		}
		
		

        if (d_consent !== undefined) {
            if (d_birthday != "" && d_gender != "" && d_visual != "") {
                data_current = {
                    'type': 'info',
                    'screen_width': window.innerWidth,
                    'screen_height': window.innerHeight,
                    'ua': navigator.userAgent,
                    'consent': d_consent,
                    'birthday': d_birthday,
                    'gender': d_gender,
                    'visual': d_visual,
                    'ident': d_ident
                };
                saveData();
                $('#instruction_continue_text').html("start");
                page++;
            } else {
                $('#message').html('Please fill out the form before continuing.').fadeIn(500).delay(1500).fadeOut(500);
            }
        } else {
            $('#message').html('Please accept the consent form, before continuing. ').fadeIn(500).delay(1500).fadeOut(500);
            $("#consent_n").prop("checked", true);
            $("input[name='consent']").checkboxradio('enable');
            $("input[name='consent']").checkboxradio('refresh');
            page = 2;
        }

    } else if (page == 4 && direction == 'continue') {
        if (cam.initialized == 1) {
            $('#instruction').fadeOut(1000);
            setTimeout("prepareBlock();", 2000);
        }
    } else if (page == 4 && direction == 'pause') {
        $('#instruction_continue').html("continue").css({'font-size': '1.7em'});
        $('#instruction_4').find("h1").html('short pause (block ' + block_no + ' of ' + design.blocks.length + ")");
        $('#setup_first').hide();
        $('#setup_after').show();

        $('#instruction').show(function() {
            if (block_no == design.blocks.length) {
                page++;
            } else {
                $('#instruction_4').fadeIn(300);
                $('#webgazerVideoFeed').show();
            }
        });
    } else if  (direction == 'continue') {
        page++;
    } else if (direction == 'back') {
        page--;
    }
    page = page < 1 ? 1 : page;
    page = page > $('.instruction_page').length ? $('.instruction_page').length : page;
    page <= 1 ? $('#instruction_back').hide() : $('#instruction_back').show();
    page >= $('.instruction_page').length ? $('#instruction_continue').hide() : $('#instruction_continue').show();
    page >= 5 ? $('#instruction_back,#instruction_continue').hide() : "";
    block_no > 0 ? $('#instruction_back').hide() : "";

    if (oldpage != page) { // if we stay at the same page, we avoid unnecessary animations
        $('.instruction_page').hide();
        $('#instruction_'+page).fadeIn(300);
    }

    // start up webcam
    if (page == 4 && cam.initialized == 0) {
        loadWebgazer();
    }

    oldpage = page;
}


var cl;
var t_start = new Date().getTime();
$('document').ready(function() {
    $('#stimulus').hide();
    $('#calibration_dot').hide();
    $('#setup_after').hide();
    $('#instruction_message').hide();
    $('#therest').hide();


    $('#start_button').click(function() {
        $(this).hide();
        prepareBlock();
    });

    $('body').keypress(function(e) {
        //e.preventDefault();
        switch(e.keyCode) {

        }
    });

    $('#instruction_continue').click(function() {
        navigation('continue');
    });

    $('#instruction_back').click(function() {
        navigation('back');
    });

    $( "#f_crowdflowerid" ).tooltip({
        show: {
            effect: "slideDown",
            delay: 250
        }
    });

    $('#takephoto_n').click(function() {
        takePhoto('no');
    });

    $('#takephoto_y').click(function() {
        takePhoto('yes');
    });

    $('#sendemail').click(function() {
        sendEmail();
    });

    /*
    $('#f_birthday').datepicker({
        dateFormat: 'yy/mm/dd',
        changeYear: true,
        changeMonth: true,
        yearRange: "-100:+0"
    });
    */
    var select = $('#f_birthday');
    for (var i=18;i <= 100; i++){
        select.append('<option value="'+i+'">'+i+'</option>')
    }

    window.localStorage.clear();
    
    var ss = window.location.hash.substring(1);
    $('#cf_reference,#asd_reference,#rub_reference,#cf_code').hide();
    if (ss == "cf") { // crowdflower-reference
        $('#cf_reference,#cf_code').show();
    } else if (ss == "rub") {
        $('#rub_reference').show();
	} else {		
        $('#asd_reference').show();
	}

    var is_chrome = navigator.userAgent.toLowerCase().indexOf('chrome') > -1;
    var is_firefox = navigator.userAgent.toLowerCase().indexOf('firefox') > -1;
    if (is_chrome || is_firefox) {
        page = 0;
        navigation('start');
    } else {
        $('#instruction').hide();
        $('#message').html('Thank you very much for your interest in our study.<br /><br />Unfortunately, your browser is not supported by our website. To participate, you need either the browser "Google Chrome" or "Firefox".<br /><br />Do download one of these securely and free of charge, please follow one of these links: <a href="https://www.google.com/chrome/browser/desktop/" target="_blank">Google Chrome</a> or <a href="https://www.mozilla.org/de/firefox/new/" target="_blank">Mozilla Firefox</a>').show();
    }
});


/**
 function drawLoop() {
    requestAnimFrame(drawLoop);
    var p = webgazer.getCurrentPrediction();
    if (p !== null) {
        console.log(p);
        $('body').append('<span class="p" style="top: '+p.y+'px; left: '+p.x+'px"></span>');
        measurements++;
    }
    t = (new Date().getTime() - start)/1000;
    cam.overlay.getContext('2d').clearRect(0,0,cam.width,cam.height);
    if (cl.getCurrentPosition()) {
        //console.log(cl.getCurrentPosition()[0]);
        //cl.draw(overlay);
    }
}
 */




window.onbeforeunload = function() {
    //webgazer.end(); //Uncomment if you want to save the data even if you reload the page.
}