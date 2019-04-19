/**
 * Common utility values and functions for task
 */

//////////////////////////////////////////
// Reuseable stimuli
// ------------------------

// HTML for text plugin
var spacebar_html = "<code>&lt;SPACEBAR&gt;</code>";
var continue_html = "<p>Press the " + spacebar_html + " to continue.</p>";
var begin_html = "<p>Press the " + spacebar_html + " to begin the task.</p>";



//////////////////////////////////////////
// vars
// ------------------------
//images----
var cue_index;
var currentTrialArray;

//ratio for scaling stimulus image if screen height is too small to display the task
//window innerHeight -height of the viewport that shows the website
if (window.innerWidth < 1400) {
	var scaleImage = (window.innerWidth) / 1400
} else {
	var scaleImage = 1;
}

// stimuli width, height, y-axis
var stimh = settings.stimulus_size[0];
var stimw = settings.stimulus_size[1];
var hstimh = stimh / 2;
var hstimw = stimw / 2;
var stimy = ((settings.canvas_height / 2) - (stimh / 2))

//stimulus size and location
var display_locs = [[0, (stimy)], [(settings.canvas_width - stimw), (stimy)]];

//fixation width and height
var fix_w = (settings.fixation_size[0]);
var fix_h = (settings.fixation_size[1]);

//fixation coordinates
var fix_xy = [((settings.canvas_width / 2) - (fix_w / 2)), ((settings.canvas_height / 2) - (fix_w / 2))]

//check if chrome - for outputting heap size
if (browser == 'Chrome') {
	var heap_used = (window.performance.memory.usedJSHeapSize / 1000000 + "MB")
	var heap_limit = (window.performance.memory.jsHeapSizeLimit / 1000000 + "MB")
} else {
	heap_used = '-1';
	heap_limit = '-1';
}

///----------task design----------///
//create pofa trials for block
function all_pofa_trials(){
	pofa_task = {};
	//task
	console.log('settings.blocks: ' + settings.blocks)
	for (var j = 0; j <= (settings.blocks); ++j) {
		//blocks
		var pofa_block = {};
		//generate two random trials and add to trialNum to make 12 trials
		rand = _.shuffle([0,1,2,3,4,5,6,7,8,9]).slice(8)
		trialNum = _.shuffle([0,1,2,3,4,5,6,7,8,9,rand[0],rand[1]])
		for (var i = 0; i <= (trialNum.length-1); ++i) {
			//trials
			pofa_trial = pofa[trialNum[i]];
			pofa_block["p"+i] = pofa_trial;
		};
		pofa_task[j] = pofa_block;
	};
	return pofa_task;
};

//create iaps trials for block
var iaps_block = [];
function all_iaps_trials(){
	iaps_task = {};
	//task
	for (var j = 0; j <= (settings.blocks); ++j) {
		//blocks
		var iaps_block = {};
		trialNum = _.shuffle([0,1,2,3,4,5,6,7,8,9])
		n = _.shuffle(['n0','n1','n2','n3','n4','n5','n6','n7','n8','n9'])
		s = _.shuffle(['s0','s1','s2','s3','s4','s5','s6','s7','s8','s9'])
		for (var i = 0; i <= (trialNum.length-1); ++i) {
			//trials
			_n = n[i]
			_s = s[i]
			iaps_trial = {
				Description: iaps[_n].Description + "-" + iaps[_s].Description,
				Duration: 4500,
				Neutral: iaps[_n].Image,
				NeutralDirectory: iaps[_n].Directory,
				NeutralDescription: iaps[_n].Description,
				NeutralID: iaps[_n].imgNum,
				Sad: iaps[_s].Image,
				SadDirectory: iaps[_s].Directory,
				SadDescription: iaps[_s].Description,
				SadID: iaps[_s].imgNum,
				Type: 'iaps',
				id: iaps[_n].imgNum + "-" + iaps[_s].imgNum
			}
			iaps_block["i"+i] = iaps_trial;
		};
		iaps_task[j] = iaps_block;
	};
	return iaps_task;
};

//combining pofa with iaps
function all_task_trials(){
	merge_iaps = all_pofa_trials();
	merge_pofa = all_iaps_trials();
	merge_task = _.merge({}, merge_iaps, merge_pofa)
	return merge_task
};

///----------for eyetracking----------///
///----------getting output of luminance----------///
//image webcam frame
var img;
var brightness;
var lumin;

function snapshot() {
	var ctx = webgazerVideoCanvas.getContext('2d');
	var img = webgazerVideoCanvas.toDataURL('image/png');
	ctx.drawImage(webgazerVideoFeed, 0, 0, webgazerVideoCanvas.width, webgazerVideoCanvas.height);
	//opens new window with image from webcam
	//window.open(img, 'test');
	getImageBrightness(img, function (brightness) {
		lumin = brightness
	});
};

//image luminance
function getImageBrightness(imageSrc, callback) {
	var img = document.createElement('img'),
		colorSum = 0,
		i = 0,
		len, canvas, ctx, imageData, data, brightness, r, g, b, avg;
	img.src = imageSrc;
	img.style.display = 'none';
	img.onload = function () {
		canvas = document.createElement('canvas');
		canvas.width = this.width;
		canvas.height = this.height;
		ctx = canvas.getContext('2d');
		ctx.drawImage(this, 0, 0);
		imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
		data = imageData.data;
		for (i, len = data.length; i < len; i += 4) {
			r = data[i];
			g = data[i + 1];
			b = data[i + 2];
			avg = Math.floor((r + g + b) / 3);
			colorSum += avg;
		}
		brightness = Math.floor(colorSum / (this.width * this.height));
		subject.lum = (brightness / 255);
		callback(brightness);
	};
}

///----------using webworker----------///
///----------for eyetracking----------///
//1.) custom event listener to begin webworker once task starts
//create custom event
var sampling_listener;
function createEvent() {
	console.log('%ccustom event for WebWorker created.','color: blue')
	sampling_listener = new CustomEvent("task_start", {});

	//event listener
	document.addEventListener("task_start", function (e) {
		//The object that receives a notification
		start_sampling();
	});
};

//2.) create webworker
var sample_array = [];
var sample_event;
var sampleNum = 0;
var sample_time;
var my_worker;
var task_event = 'Fixation'; ////for sample_array debugging (know what events occured when gaze sample was collected)
function start_sampling() {
	if (window.Worker) { // Check if browser supports the Worker api.
		console.log('%cWebWorker function started.','color: blue')
		var testing = document.querySelector('.testing');
		//creating worker
		my_worker = new Worker('src/js/worker/worker.js');
		//Method called by worker
		my_worker.onmessage = function (e) {
			if (end_trial_data == false) {
				current_time = performance.now();
				sample_time = Math.round(current_time - start_time);
				//check if null eye data
				try {
					gaze_x;
					gaze_y;
				} catch (err) {
					console.log('coordinates failed')
					gaze_x = -1;
					gaze_y = -1;
				}
				sample_event = {
					trialNumTask: trialNumTask,
					sampleNum: sampleNum,
					x: gaze_x,
					y: gaze_y,
					sample_time: sample_time,
					event: task_event
				};
				sample_array.push(sample_event);
				sampleNum = sampleNum + 1;
				//console.log(e.data);
			};
		};
	};
}

//----------for eyetracking----------///
///---------combine behavioral and eyetracking data----------///
function merge_array(practice_data, behavioral_data, sample_data) {
	var new_array = practice_data;
	for (var i = 0; i < (sample_data.length); i++) {
		//get trial number
		_trialNum = sample_data[i].trialNumTask;
		//merge behavioral information (at trial #) with eyetracking
		_result = $.extend(true, {}, behavioral_data[_trialNum], sample_data[i]);
		new_array.push(_result);
	};
	return new_array;
};

//////////////////////////////////////////
// Functions
// ------------------------
////////////////////
//loadingbar
var width = 4
var loading = new ProgressBar.Circle('#progress', {
	color: '#ffffff',
	// This has to be the same size as the maximum width to
	// prevent clipping
	strokeWidth: width,
	trailWidth: width,
	easing: 'linear',
	duration: 0,
	from: {
		color: '#ff0000',
		width: width
	},
	to: {
		color: '##00ff00',
		width: width
	},
	// Set default step function for all animate calls
	step: function (state, circle) {
		circle.path.setAttribute('stroke', state.color);
		circle.path.setAttribute('stroke-width', state.width);

		var value = Math.round(circle.value() * 100);
		if (value === 0) {
			circle.setText('');
		} else {
			circle.setText(value + "%");
		}
	}

});
loading.text.style.fontFamily = 'Calibri, Candara, Segoe, "Segoe UI", Optima, Arial, sans-serif';
//loading.text.style.fontSize = '2rem';

//check if user switches tabs in browser window
var vis = (function () {
	var stateKey, eventKey, keys = {
		hidden: "visibilitychange",
		webkitHidden: "webkitvisibilitychange",
		mozHidden: "mozvisibilitychange",
		msHidden: "msvisibilitychange"
	};
	for (stateKey in keys) {
		if (stateKey in document) {
			eventKey = keys[stateKey];
			break;
		}
	}
	return function (c) {
		if (c) document.addEventListener(eventKey, c);
		return !document[stateKey];
	}
})();

/*heatmap*/
var bins;
function heatmap(raw_data) {
	//check if div exists
	if ($('#heatmap').length){
		$('#heatmap').remove();
	};
	//filter by trial
	raw_data_filter = _.filter(raw_data, {trialNumTask: trialNumTask})
    // preprocess data for heatmap
    bins = []; // create bins and fill them
    for (var y = 0; y < window.innerHeight; y++) {
        for (var x = 0; x < window.innerWidth; x++) {
            bins.push([x, y, 0]);
        }
    }
    // sort fixations into bins and get max
    var max = 0;
    for (var i = 0; i < raw_data_filter.length - 1; i++) {
        var d = raw_data_filter[i];
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
    $("#heatmap").css({top: 0, left: 0, position:'absolute'});
    heat = simpleheatmap('heatmap');
    heat.resize();
    heat.radius(30,50);
    heat.max(max).data(binsc).draw();
}


/*get gpu*/
var gpu;
function getGPU() {
	$(document).ready(function () {
		//check if supported and enabled
		if (!!window.WebGLRenderingContext) {
			canvas_available = document.getElementById('renderCanvas');
			console.log(canvas_available)
			gl = canvas_available.getContext("webgl") || canvas_available.getContext("experimental-webgl");
			if (gl && gl instanceof WebGLRenderingContext) {
				//if yes, get gpu //https://developer.mozilla.org/en-US/docs/Web/API/WEBGL_debug_renderer_info
				gl = canvas_available.getContext('webgl');
				debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
				gpu = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
				//unsupported
			} else {
				gpu = -1;
			};
			//disabled
		} else {
			gpu = -1;
		}
	})
};

//check fullscreen
//at each trial check if fullscreen #if not prompt user and store isFullscreen in csv file
///window.screen.height = size of monitor height; window.innerHeight = size of browser viewport height; 
//https://developer.mozilla.org/en-US/docs/Web/API/Screen/height
//https://developer.mozilla.org/en-US/docs/Web/API/Window/outerHeight
//https://stackoverflow.com/questions/16162639/difference-between-screen-and-window-property
function printDimensions() {
	console.log("window.innerHeight: "+window.innerHeight)
	console.log("window.outerHeight: "+window.outerHeight)
	console.log("window.screen.height: "+window.screen.height)
	console.log("window.innerWidth: "+window.innerWidth)
	console.log("window.outerWidth: "+window.outerWidth)
	console.log("window.screen.width: "+window.screen.width)
};

var isFullscreen;
function checkfullscreen() {
	if ((window.innerHeight < (.85*window.screen.height)) && (window.innerWidth < (.85*window.screen.width))) {
		if (debug){
			console.log('%cnot fullscreen','color: orange');
			console.log('%cexperiment paused','color: orange');
			printDimensions()
		};
		$("#jspsych-stim-canvas").hide()//hide canvas
		isFullscreen = false; //set fullscreen false for trial
		$notFullscreen = $(
							"<div style=''>"+
							"<p>We detected that the task may no longer be in fullscreen mode.</p>"+
							"<p>The experiment will continue in fullscreen mode when you click the button below.</p>"+
							"<button id='jspsych-fullscreen-btn' class='jspsych-btn'>Fullscreen</button>"+
							"</div>")
		$($notFullscreen).appendTo("#jspsych-content");
		$('body').css('cursor',"auto"); //turning cursor back on
		jsPsych.pauseExperiment();
		//if fullscreen button clicked and continue task
		$('#jspsych-fullscreen-btn').on('click', function() {
			console.log('Fullsreen clicked')
			//initiate fullscreen
			var element = document.documentElement;
			if (element.requestFullscreen) {element.requestFullscreen()}
			else if (element.mozRequestFullScreen) {element.mozRequestFullScreen()}
			else if (element.webkitRequestFullscreen) {element.webkitRequestFullscreen()}
			else if (element.webkitRequestFullScreen) {element.webkitRequestFullScreen()}
			else if (element.msRequestFullscreen) {element.msRequestFullscreen()};
			//continue task
				$('#jspsych-fullscreen-btn').off('click');
				console.log('%cnext trial','color: blue');
				$('body').css('cursor',"none"); //turning cursor back on
				$($notFullscreen).remove()//hide message
				$("#jspsych-stim-canvas").show()//show canvas
				jsPsych.resumeExperiment()//resume experiment
			});
	} else {
		if (debug){
			console.log('%cfullscreen','color: green');
			printDimensions()
		};
		isFullscreen = true;
	};
};

//run break before begining block 4 and block 6
function isBreak(){
	//update server with portion of task
	(function() {
		if (subject.webcam_used == true) {
			webgazer.pause(); //pause webgazer while in break
			console.log('%csubsession: '+pid.subsession,'color: blue');
			saveData(participant_id + "_" + pid.session + pid.subsession + ".csv", jsPsych.data.forServer());
		} else {
			console.log('%csubsession: '+pid.subsession,'color: blue');
			saveData(participant_id + "_" + pid.session + pid.subsession + ".csv", jsPsych.data.dataAsCSV());
		}
	})();
	console.log('%cBreak','color: red')
	console.log('%cexperiment paused','color: orange');
	$("#jspsych-stim-canvas").hide() //hide canvas
	$Break = $("<div style=''>"+
				"<p>You now have a brief break.</p>"+
				"<p>The experiment will continue when you click the button below.</p>"+
				"<button id='jspsych-fullscreen-btn' class='jspsych-btn'>Continue</button>"+
				"</div>")
	$($Break).appendTo("#jspsych-content");
	$('body').css('cursor',"auto"); //turning cursor back on
	jsPsych.pauseExperiment(); //pause experiment
	//if fullscreen button clicked and continue task
	$('#jspsych-fullscreen-btn').on('click', function() { 
		console.log('Continue clicked')
		//continue task
		$('#jspsych-fullscreen-btn').off('click');
		console.log('%cnext trial','color: blue');
		$('body').css('cursor',"none"); //turning cursor back on
		$($Break).remove(); //hide message
		$("#jspsych-stim-canvas").show(); //show canvas
		if (subject.webcam_used == true){webgazer.resume()}; //resume webgazer after break
		jsPsych.resumeExperiment(); //resume experiment
	});
};

// sum a list of values
function sum(list) {
	return _.reduce(list, function (memo, num) {
		return memo + num;
	});
}

// convert milliseconds to minutes, rounding up
function millisecondsToMinutes(ms) {
	return Math.ceil(ms / 1000 / 60);
}

// get url parameters
var urlparam;
function getUrlParams() {
	uri = new URI(window.location.href);
	//var ID = uri.fragment();
	//return ID;
	urlparam = uri.search(true);
	if (_.isEmpty(urlparam)){
		urlparam = null;
		console.log('%c2-3.getUrlParams() failed','color: red');
		EmailFail();
	} else {
		urlparam.rtco = Number(urlparam.rtco);
		console.log('%c2-3.getUrlParams() success','color: green');
	};
	return urlparam;
}

// try to get a participant ID
function getParticipantId() {
	// first attempt to get PID via URL params
	console.log('%c2-2.attempting getUrlParams()...','color: orange');
	sub_idc = getUrlParams();
	// then use window prompt
	//sub_idc = sub_idc || window.prompt("Please enter your ID");
	// as a last resort, generate a jsPsych random ID
	if (debug){
		sub_idc = sub_idc || {uname: jsPsych.randomization.randomID().substring(0,6), code: _.shuffle(['AAA','BBB'])[0], rtco:1};
	};
	return sub_idc;
};


//check database for subject id and session number
//if new subject, prepare pid
var pid, db_compare, participant_id, start_task, isAdmin, idc, condition;
var cndt_code = {'active':'a','placebo':'b','wait':'c','missing':'d'};//make condition code into non meaningful text
function getDatabase() {
	//<-- see returning Deferred object
	return d1 = $.Deferred (function(){
		console.log('%c2-1.attempting getDatabase()...','color: orange');
		idc = getParticipantId();
		participant_id = idc.uname;
		console.log('%c3.getParticipantId() success','color: green',idc);
		//check database for subject data
		$.ajax({
				url: "src/php/get.php",
				type: 'post',
				data: {
					subject: participant_id,
					code: idc.code,
				},
				dataType: "JSON",
				processData: true
			})
			.done(function (response) {
				console.log('%c4.getDatabase() success','color: green');
				console.log(response);
				db_compare = response;
				isAdmin = db_compare[0].isAdmin;
				condition = db_compare[0].condition; //active, placebo, wait, missing (i.e. no matching code/condition pairs)
				//if new subject //create row with 0 session
				if (db_compare[0].ready == 'new') {
					console.log('%c5.new subject','color: green');
					//resolve deferral
					start_task = true;
					pid = {
						'subject': participant_id,
						'session': 0,
						'subsession': 'a',
						'start_time': 0,
						'end_time': 0,
						'code': idc.code,
						'location': db_compare[0].location,
						'score': 0,
						'eyetracking': '',
						'finished':'',
						'uploaded':'',
						'slow': '',
						'baseline': Number(idc.rtco)
					};
					//if condition missing
					if (db_compare[0].condition == 'missing'){
						sessionfail();
					} else {
						//begin experiment
						d1.resolve();
					}
				//else old subject
				} else {
					//if condition missing
					if (db_compare[0].condition == 'missing'){
						sessionfail();
					} else {
						//if subject participated less then 24 hours ago
						if (db_compare[0].ready == 'wait'){
							console.log('%c5.x<24hr limit','color: red');
							//resolve deferral
							start_task = false;
							//load new page
							wait_until(db_compare[0].start_date, db_compare[0].wait_date);
							d1.catch();
						//enough time has passed since participating last
						} else {
							console.log('%c5.old subject','color: green');
							//resolve deferral
							start_task = true;
							pid = {
								'subject': participant_id,
								'session': Number(db_compare[0].subject_session) + 1,
								'subsession': 'a',
								'start_time': 0,
								'end_time': 0,
								'code': idc.code,
								'location': db_compare[0].location,
								'score': 0,
								'eyetracking': db_compare[0].eyetracking,
								'finished':'',
								'uploaded':'',
								'slow': 'false',
								'baseline': Number(db_compare[0]["baseline"])
							};
							//begin experiment
							d1.resolve();
						};
					}
				}
			})
			.fail(function (response) {
				console.log(response)
				//resolve deferral
				start_task = false
				//getting subject number failed //cancel task
				console.log('%c4.getDatabase() failed - cancelling task','color: red');
				//load new page //if get subject failed, let participant know
				d1.catch();
				sessionfail();
			})
	});
}

//once task finishes post new row to database
function postDatabase() {
	$.ajax({
		url: "src/php/post.php",
		type: 'post',
		data: pid,
		dataType: "JSON",
		processData: true,
	})
	.done(function (response) {
		console.log('%c5-1.postDatabase() success','color: green');
		console.log(response);
		//if wait condition
		if (condition == "wait"){
			console.log('%c5.1.wait condition','color: green');
			window.location.href = "http://www.google.com";
		};
		if ((!isNaN(pid.score) && !isNaN(pid.baseline)) && (pid.score >= pid.baseline) && (pid.finished)) {
			console.log('%c5.1.improved score','color: green');
			EmailBaseline();
		};
	})
	.fail(function (response) {
		console.log('%c5-1.postDatabase() failed','color: red');
		console.log(response)
	})
}

//post email if issue running task
function EmailFail() {
	$.ajax({
		url: "src/php/email.php",
		type: 'post',
		data: {
			purpose: 'fail',
			reason: 'incorrect uri parameters',
			url: window.location.href
		},
		dataType: "JSON",
		processData: true,
	})
	.done(function(response){
		console.log('%c11.EmailFail() success','color: green');
		document.write(
			'<script src="dist/js/jquery-3.1.0.min.js"></script>' +
			'<link href="dist/css/jspsych.css" rel="stylesheet" type="text/css">' +
			'<link href="dist/css/experiment.css" rel="stylesheet" type="text/css">' +
			'<div class="container">' +
			'<div class="container-inner">' +
			'<p>There seems to be an issue running the experiment.</p>' +
			'<p>Please notify the researchers at comparemindtrial@utexas.edu.</p>'
		);
	})
	.fail(function(jqXHR, textStatus, error, response){
		console.log('%c11.EmailFail() failed','color: red');
	})
};

//post email if current session score >= baseline  
function EmailBaseline() {
	$.ajax({
		url: "src/php/email.php",
		type: 'post',
		data: {
			purpose: 'rtco',
			subject: pid.subject, 
			session: pid.session + '-' + pid.subsession, 
			end_time: pid.end_time, 
			score: pid.score, 
			baseline: pid.baseline
		},
		dataType: "JSON",
		processData: true,
	})
	.done(function (response) {
		console.log('%c11.EmailBaseline() success','color: green');
	})
	.fail(function(jqXHR, textStatus, error, response){
		console.log('%c11.EmailBaseline() failed','color: red');
	})
};

//redirect back to SONA
function redirectSona() {
	id_redirect = '&survey_code=' + participant_id
	$(location).attr('href', 'https://utexas.sona-systems.com/webstudy_credit.aspx?experiment_id=471&credit_token=1c15f6958b8844c8be1f69c041a68dbe' + id_redirect)
};

//check if more than 30% of subject trials have long RT and/or no resp, mark as slow on db
function checkPerformance(){
	if (lslow.length >= (.30*ltask_acc.length)){
		isSlow = "true"
	} else {
		isSlow = "false"
	}
	return isSlow
}

//set emoji in feedback
var PID_emoji;
function checkPID(){
	//check if pid.score >= pid.baseline
	//if (pid.score >= pid.baseline){
	if (pid.score >= pid.baseline){
		PID_emoji = '<div class="imgContainer">' +
							'<img src="dist/img/sad.png" height="150" width="150"/>' +
					'</div>'
	} else {
		PID_emoji = '<div class="imgContainer">' +
						'<img src="dist/img/happy.png" height="150" width="150"/>' +
					'</div>'
	};	
};

// post data to the server using an AJAX call
var taskEnd; //experiment end time
function saveData(filename, filedata) {
	//get end timestamp
	pid.end_time = (new Date(Date.now() - ((new Date()).getTimezoneOffset() * 60000))).toISOString();
	if (ltask_acc.length==0){
		pid.score = Number(-1);
		checkPID();
	} else {
		pid.score = Number((_.sum(ltask_acc)/_.mean(lrt))*1000)
		checkPID()
	};
	pid.eyetracking = subject.webcam_used;
	pid.slow = checkPerformance();
	console.log("trial count: "+jsPsych.data.getTrialsOfType("dotprobe-task").length)
	if (jsPsych.data.getTrialsOfType("dotprobe-task").length == task.length){
		pid.finished = "true";
	} else {
		pid.finished = "false";
	};
	console.log("subject: ", filename);
	$.ajax({
		url: "src/php/upload.php", // this is the path to the above PHP script
		type: 'post',
		data: {
			fname: filename,
			fdata: filedata,
			subsession: pid.subsession
		},
		processData: true
	})
	.done(function(response){
		pid.uploaded = 'true'; //file was successfully uploaded
		//if break is over
		console.log('%cis pid finished: %s','color: blue',pid.finished);
		if (jsPsych.data.getTrialsOfType("dotprobe-task").length == task.length){
			alert("Data was successfully saved.");
			console.log("Data was successfully saved.");
			if (debug){
				document.write(
					'<script src="dist/js/jquery-3.1.0.min.js"></script>' +
					'<link href="dist/css/jspsych.css" rel="stylesheet" type="text/css">' +
					'<link href="dist/css/experiment.css" rel="stylesheet" type="text/css">' +
					'<div class="container">' +
					'<div class="container-inner">' +
					'<p>You have completed the task!</p>' +
					'<p>Your score for this session is '+pid.score+'.</p>' +
					'<p>While your score from baseline is '+pid.baseline+'.</p>' + PID_emoji
				)
			} else {
				document.write(
					'<script src="dist/js/jquery-3.1.0.min.js"></script>' +
					'<link href="dist/css/jspsych.css" rel="stylesheet" type="text/css">' +
					'<link href="dist/css/experiment.css" rel="stylesheet" type="text/css">' +
					'<div class="container">' +
					'<div class="container-inner">' +
					'<p>You have completed the task!</p>'+
					'<p>Your score for this session is '+pid.score+'.</p>' + PID_emoji
				)}
			}
			//save local
			if (debug) {
				saveLocalCSV(filedata, participant_id + "_" + pid.session + pid.subsession + ".csv", 'csv');
				postDatabase();//post participation to database
			} else {
				postDatabase();//post participation to database
				//setTimeout(redirectSona, 10000);//added setTimeout as redirect back to Sona
			}

	})
	.fail(function(jqXHR, textStatus, error, response){
		pid.uploaded = 'false'; //file not successfully uploaded
		document.write(
			'<script src="dist/js/jquery-3.1.0.min.js"></script>' +
			'<link href="dist/css/jspsych.css" rel="stylesheet" type="text/css">' +
			'<link href="dist/css/experiment.css" rel="stylesheet" type="text/css">' +
			'<div class="container">' +
			'<div class="container-inner">' +
			'<p>You have completed the task!</p>' +
			'<p>Your score for this session is '+pid.score+'.</p>' +
			'<p>But your results have not been successfully saved to our server.</p>' +
			'<p>Please download the following file and email to comparemindtrial@utexas.edu.</p>'
		);
		//save local
		if (debug) {
			saveLocalCSV(filedata, participant_id + "_" + pid.session + pid.subsession + ".csv", 'csv');
			postDatabase();//post participation to database
		} else {
			saveLocalCSV(filedata, participant_id + "_" + pid.session + pid.subsession + ".csv", 'csv');
			postDatabase();//post participation to database
			//setTimeout(redirectSona, 10000);//added setTimeout as redirect back to Sona
		};
	})
};

/*save locally if server failed*/
function saveLocalCSV(text, name, type) {
	var a = document.createElement("a");
	var file = new Blob([text], {
		type: type
	});
	a.href = URL.createObjectURL(file);
	a.download = name;
	a.click();
};