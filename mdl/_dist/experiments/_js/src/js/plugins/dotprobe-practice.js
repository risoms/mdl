/**
 * dotprobe-practice
 **/
var practice_acc = []; //accuracy list for each trial
var cue_images;
var prac_avg;
jsPsych.plugins["dotprobe-practice"] = (function () {

	var plugin = {};

	jsPsych.pluginAPI.registerPreload('dotprobe-practice', 'stimulus', 'image', function (t) {
		return !t.is_html || t.is_html == 'undefined'
	});

	plugin.info = {
		name: 'dotprobe-practice',
		description: '',
		parameters: {
			stimulus: {
				type: [jsPsych.plugins.parameterType.STRING],
				default: undefined,
				no_function: false,
				description: ''
			},
			is_html: {
				type: [jsPsych.plugins.parameterType.BOOL],
				default: false,
				no_function: false,
				description: ''
			},
			choices: {
				type: [jsPsych.plugins.parameterType.KEYCODE],
				array: true,
				default: jsPsych.ALL_KEYS,
				no_function: false,
				description: ''
			},
			prompt: {
				type: [jsPsych.plugins.parameterType.STRING],
				default: '',
				no_function: false,
				description: ''
			},
			timing_stim: {
				type: [jsPsych.plugins.parameterType.INT],
				default: -1,
				no_function: false,
				description: ''
			},
			timing_response: {
				type: [jsPsych.plugins.parameterType.INT],
				default: -1,
				no_function: false,
				description: ''
			},
			response_ends_trial: {
				type: [jsPsych.plugins.parameterType.BOOL],
				default: true,
				no_function: false,
				description: ''
			},

		}
	}

	plugin.trial = function (display_element, trial) {
		// if any trial variables are functions
		// this evaluates the function and replaces
		// it with the output of the function
		trial = jsPsych.pluginAPI.evaluateFunctionParameters(trial);

		// set default values for the parameters
		trial.choices = trial.choices || jsPsych.ALL_KEYS;
		trial.response_ends_trial = (typeof trial.response_ends_trial == 'undefined') ? true : trial.response_ends_trial;
		trial.timing_stim = trial.timing_stim || -1;
		trial.timing_response = trial.timing_response || -1;
		trial.is_html = (typeof trial.is_html == 'undefined') ? false : trial.is_html;
		trial.prompt = trial.prompt || "";

		//getting trialNum
		var trialvalue = prac_trial_value;

		//getting pracTrial
		///shuffle pracBlock at each iteration
		if (iteration_finished == true) {
			pracBlock = jsPsych.randomization.shuffle(pracBlock);
			if (debug){console.log('shuffled block:', pracBlock)};
		}
		pracTrial = pracBlock[trialvalue];

		//iteration finished - used to break practice loop_function (gaze.js)
		iteration_finished = false;

		//timeout to allow svg to finish (msec)
		var delay = (function () {
			var timer = 0;
			return function (callback, ms) {
				clearTimeout(timer);
				timer = setTimeout(callback, ms);
			};
		})();

		// store response
		var response = {
			rt: -1,
			key: -1,
			resp: -1
		};

		//if first trial in experiment
		//draw canvas once
		if (first_practice == true) {
			//get start timestamp
			pid.start_time = (new Date(Date.now() - ((new Date()).getTimezoneOffset() * 60000))).toISOString();
			//close event
			first_practice = false;
			//hide mouse
			$('body').css('cursor', 'none');
			//draw canvas
			var svg = d3.select("#jspsych-content").append("svg")
				.attr('id', 'jspsych-stim-canvas')
				.attr('display', 'block')
				.attr('vertical-align', 'middle')
				.attr('margin', 'auto')
				.attr("width", settings.canvas_width * scaleImage)
				.attr("height", settings.canvas_height * scaleImage);
			//draw fixation
			left_right = ['left', 'right']
			var img = svg.append("svg:image")
				.attr('id', 'jspsych-fixation-image')
				.attr("xlink:href", ("src/img/fixation.png"))
				.attr("x", fix_xy[0] * scaleImage)
				.attr("y", fix_xy[1] * scaleImage)
				.attr("width", fix_w * scaleImage)
				.attr("height", fix_h * scaleImage);

			//draw stim
			for (var i = 0; i < display_locs.length; i++) {
				var img2 = d3.select("#jspsych-stim-canvas").append("svg:image")
					.attr('id', 'jspsych-image-' + left_right[i])
					.attr("xlink:href", (settings.element_directory + settings.mask_image))
					.attr("x", (display_locs[i][0] * scaleImage))
					.attr("y", (display_locs[i][1] * scaleImage))
					.attr("width", (stimw * scaleImage))
					.attr("height", (stimh * scaleImage))
			}

			//checking display window size
			subject.display_window = [window.innerWidth + "x" + window.innerHeight];

		} else {
			//update canvas to replace cue
			$("#jspsych-stim-canvas").removeClass('responded')
				.attr("width", settings.canvas_width * scaleImage)
				.attr("height", settings.canvas_height * scaleImage);
			$("#jspsych-fixation-image")
				.attr("x", fix_xy[0] * scaleImage)
				.attr("y", fix_xy[1] * scaleImage)
				.attr("width", fix_w * scaleImage)
				.attr("height", fix_h * scaleImage);
			var img = d3.select("#jspsych-image-" + cue_index)
				.attr("xlink:href", (settings.element_directory + settings.mask_image))
		}
		
		//trial onset time
		start_time = performance.now();
		trial.start_t = start_time;
		
		
		////////////////////////////1.show fixation
		show_fixation();
		function show_fixation() {
			task_event = 'Fixation'; ////for sample_array debugging (know what events occured when gaze sample was collected)
			//show fixation
			$("#jspsych-fixation-image")[0].href.baseVal = "src/img/fixation.png"
			// duration
			setTimeout(function () {
				//clear fixation
				$("#jspsych-fixation-image")[0].href.baseVal = ""
				show_image();
			}, settings.stimulus_onset);
		}

		////////////////////////////2.show Stim
		function show_image() {
			task_event = 'Stim'; ////for sample_array debugging (know what events occured when gaze sample was collected)
			//preparing list of left and right stim for call
			trial_images = [pracTrial.LStim,pracTrial.RStim];
			
			//get facestim offset time, base on type of stim (pofa or iaps)
			if (pracTrial.trialType=='IAPS'){
				settings.stimulus_offset = settings.iaps_offset
			} else {
				settings.stimulus_offset = settings.pofa_offset
			};
			
			//start time
			var current_time = performance.now();
			trial.stim_onset = current_time - trial.start_t;
			if (debug){console.log('%ctrial_type: %s','color: blue',pracTrial.Type)
			console.log('%cstimulus onset: %smsec','color: green',trial.stim_onset)}
			
			//draw stim
			for (var i = 0; i < display_locs.length; i++) {
				var img = d3.select("#jspsych-image-" + left_right[i])
				.attr('id', 'jspsych-image-' + left_right[i])
				.attr("xlink:href", (settings.element_directory + 'stim/' + trial_images[i]))
				.attr("x", (display_locs[i][0]*scaleImage))
				.attr("y", (display_locs[i][1]*scaleImage))
				.attr("width", (stimw*scaleImage))
				.attr("height", (stimh*scaleImage));
			};

			// duration
			setTimeout(function () {
				//end time
				show_cue();
			}, settings.stimulus_offset);
		}

		////////////////////////////3.show DotLoc
		function show_cue() {
			task_event = 'DotLoc'; ////for sample_array debugging (know what events occured when gaze sample was collected)
			//preparing list for call
			var cue_list = jsPsych.randomization.shuffle(['cue_1.jpg', 'cue_2.jpg']);
			cue_img = cue_list[0];
			
			cue_images = [cue_img,settings.mask_image];
			//shuffling cue location
			cue_images = jsPsych.randomization.shuffle(cue_images);
			
			//start time
			var current_time = performance.now();
			trial.cue_onset = current_time - trial.start_t;
			if (debug){console.log('%ccue onset: %smsec','color: green',trial.cue_onset)};
			
			//draw stim
			for (var i = 0; i < display_locs.length; i++) {
				var img = d3.select("#jspsych-image-" + left_right[i])
				.attr("xlink:href", (settings.element_directory + cue_images[i]))
				.attr("x", (display_locs[i][0]*scaleImage))
				.attr("y", (display_locs[i][1]*scaleImage))
				.attr("width", (stimw*scaleImage))
				.attr("height", (stimh*scaleImage));
			};

			// function to handle responses by the subject
			var after_response = function (info) {
				// after a valid response, the stimulus will have the CSS class 'responded'
				$("#jspsych-content").addClass('responded');
				// only record the first response
				if (response.key == -1) {
					response = info
				}
				//create string from keycode
				if (response.key == 56 || response.key == 104) {
					response.resp = '8';
				} else if (response.key == 57 || response.key == 105) {
					response.resp = '9';
				} else {
					response.resp = -1;
				}
				
				//end trial early
				if (trial.response_ends_trial) {
					//end time
					var current_time = performance.now();
					//trial offset
					trial.end_t = current_time - trial.start_t;
					if (debug){console.log('%cend trial (early): %smsec','color: green',trial.end_t)};
					end_trial(response);
				}
			};

			//cue index location
			cue_index = cue_images.indexOf("cue_");

			// start the response listener
			keyboardListener = jsPsych.pluginAPI.getKeyboardResponse({
				callback_function: after_response,
				valid_responses: [56, 57, 104, 105],
				rt_method: 'date',
				persist: false,
				allow_held_key: false
			});

			//end trial if time limit is set
			if (trial.timing_response > 0) {
				timeout_on = setTimeout(function () {
					//end time
					var current_time = performance.now();
					//trial offset
					trial.end_t = current_time - trial.start_t;
					if (debug){console.log('%cend trial (normal): %smsec','color: green',trial.end_t)};
					var response = {
						rt: -1,
						key: -1,
						resp: -1
					}
					end_trial();
				}, settings.cue_offset);
			};
		};

		// function to end trial when it is time
		var end_trial = function () {
			//clearing the screen
			$("#jspsych-image-left")[0].href.baseVal = ""
			$("#jspsych-image-right")[0].href.baseVal = ""
			end_trial_data = true;
			//check if tab is focused
			var visible = vis();
			// kill keyboard listeners
			jsPsych.pluginAPI.cancelKeyboardResponse(keyboardListener);
			//kill timeout
			window.clearTimeout(timeout_on);

			// gather the data to store for the trial
			//.exp = expected, .real = real, .rt = resp time, .resp = resp key
			var trial_data = {
				//participant
				'participant': participant_id,
				'session': pid.session,
				'subsession': 'NaN',
				'condition': cndt_code[condition],
				'code': pid.code,
				'expName': settings.expName,
				'date': settings.date,
				'os': subject.os,
				'gpu': gpu,
				//browser
				'heap.used': heap_used,
				'heap.limit': heap_limit,
				'browser': subject.browser,
				//webcam
				'isWebcamUsed': subject.webcam_used,
				'WebcamMessage': WebcamMessage,
				'WebcamDevice': MediaDevice,
				'webcamSize.px': subject.webcam_size,
				'lum': subject.lum,
				'isWindowSuccess': isWindowSuccess,
				//screen
				'monitorSize.px': subject.display_monitor,
				'windowSize.px': subject.display_window,
				'diagonalSize.in': diagonal_inches,
				'devicePixelRatio': subject.devicePixelRatio,
				'isPageVisible': visible,
				'isFullscreen': '',
				'scaling': scaleImage,
				//eyetracking
				'sampleNum': -1,
				'sample_time': -1,
				'x': -1,
				'y': -1,
				//time
				'duration.t': Math.round(trial.end_t),
				'Stim_onset.t': Math.round(trial.stim_onset),
				'DotLoc_onset.t': Math.round(trial.cue_onset),
				//blocking
				'blockNum': -1,
				'trialNum': trialvalue,
				'trialNumTask': trialvalue,
				'trialID': pracTrial.ID,
				//resp
				'Key_Resp.rt': response.rt,
				'Key_Resp.resp': response.resp,
				'Key_Resp.cresp': '',
				'Key_Resp.acc': '',
				//trial
				'baseline': idc.rtco,
				'DotLoc': pracTrial.DotLoc,
				'LEmotion': pracTrial.LEmotion,
				'LStim': pracTrial.LStim,
				'LDescription': pracTrial.LDescription,
				'REmotion': pracTrial.REmotion,
				'RStim': pracTrial.RStim,
				'RDescription': pracTrial.RDescription,
				'trialType': pracTrial.Type,
				'isCongruent': true,
				'event': 'Prac'
			};
			
			//-------collect cresp and accuracy
			//collect cresp
			if (cue_img == "cue_2.jpg") {
				trial_data['Key_Resp.cresp'] = 9; //adding to csv
				cue_index = cue_images.indexOf("cue_2.jpg");
				//which side of screen cue is on
				if (cue_index==0){//left side of screen
					trial_data['DotLoc'] = 'LeftD'
				} else {//right-side of screen
					trial_data['DotLoc'] = 'RightD';
				};
			} else {
				trial_data['Key_Resp.cresp'] = 8 //adding to csv
				cue_index = cue_images.indexOf("cue_1.jpg");
				//which side of screen cue is on
				if (cue_index==0){//left side of screen
					trial_data['DotLoc'] = 'LeftS'
				} else {//right-side of screen
					trial_data['DotLoc'] = 'RightS';
				};
			}
			
			//if no or incorrect response
			if (response.resp == -1 || trial_data['Key_Resp.cresp'] != response.resp){
				trial_data['Key_Resp.acc'] = 0 //adding to csv
				practice_acc.push(trial_data['Key_Resp.acc'])
			} else {
				trial_data['Key_Resp.acc'] = 1 //adding to csv
				practice_acc.push(trial_data['Key_Resp.acc'])
			}
			
			//console
			if (debug){
				console.log('%ctrial end;\n'+
							'cue type: %s;\n'+
							'isCongruent: %s;\n'+
							'trial: %s;\n'+
							'block: %s;\n'+
							'iteration: %s;\n'+
							'resp: %s;\n'+
							'cresp: %s;\n'+
							'acc: %s;\n'+
							'block acc: %O',
							'color: orange',
							trial_data['DotLoc'],
							trial_data['isCongruent'],
							prac_trial_value,
							trial.block_order,
							prac_iter,
							response.resp,
							trial_data['Key_Resp.cresp'],
							trial_data['Key_Resp.acc'],
							practice_acc)};
			
			//response reset
			response = {
				rt: -1,
				key: -1,
				resp: -1
			}
			
			//check if fullscreen //isFullscreen updated within checkfullscreen function
			checkfullscreen();
			trial_data['isFullscreen'] = isFullscreen;
			trial_data['windowSize.px'] = [window.innerWidth+"x"+window.innerHeight];
			
			// use after last trial in practice
			if (trial.block_order == 'Prac' && prac_trial_value == (pracBlock.length - 1)) {
				//add iteration counter
				prac_iter = prac_iter + 1;
				//iteration finished - used to break practice loop_function (gaze.js)
				iteration_finished = true;
				//reset trial number
				prac_trial_value = 0;
				//practice average
				prac_avg = (sum(practice_acc) / practice_acc.length) * 100
				if (debug){console.log('%cblock acc: %s%','color: orange',prac_avg)};
				//reset block acc
				practice_acc = [];
				//accuracy message
				if ((iteration_finished == true) && (prac_avg < 79.9)){
					if (debug){console.log('%cblock failed','color: red')};
					$("#jspsych-stim-canvas").hide()//hide canvas
					//accuracy message
					$acc_message = $(
						"<div id=acc_message>"+
						"<p>Your accuracy for the practice session was "+Number(Math.round(prac_avg+'e2')+'e-2')+"%.</p>"+
						"<p>Please repeat the practice session to improve your accuracy.</p>"+
						"<p>Also remember: <code>8</code>=*, <code>9</code>=**.</p>"+
						"<br>"+
						"<p>Press the SPACE button when you're ready to begin.</p>"+
						"</div>")
					$($acc_message).appendTo("#jspsych-content")
					jsPsych.finishTrial(trial_data);
					jsPsych.pauseExperiment();
					if (debug){console.log('%cexperiment paused','color: orange')};
					$(window).on("keypress", function(key) {
						//if spacebar pressed
						if(key.keyCode == 32){
							if (debug){console.log('%cnext iteration','color: blue')};
							$($acc_message).remove()//hide message
							$("#jspsych-stim-canvas").show()//show canvas
							jsPsych.resumeExperiment()//resume experiment
							return plugin
						}
					})
				}
			// else next trial
			} else {
				//add next trial counter
				prac_trial_value = prac_trial_value + 1;
			}

			//if 12th iteration of experiment and acc < 55%, end task
			if (prac_iter == 12 && prac_avg < 80) {
				jsPsych.endExperiment();
			}

			//-------move on to the next trial
			jsPsych.finishTrial(trial_data);
		}
	};
	return plugin;
})();