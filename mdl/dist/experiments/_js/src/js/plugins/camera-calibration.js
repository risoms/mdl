/**
 * Set up webcam for eyetracking experiment.
 * @module camera-calibration
 */
jsPsych.plugins["camera-calibration"] = (function() {
	var plugin = {};
	jsPsych.pluginAPI.registerPreload('camera-calibration', 'stimulus', 'image', function(t) {
		return !t.is_html || t.is_html == 'undefined'
	});
	plugin.info = {
		name: 'camera-calibration',
		description: '',
		parameters: {
			stimulus: {
				type: [jsPsych.plugins.parameterType.STRING],
				default: undefined,
				no_function: false,
				description: ''
			},
			trialNum: {
				type: [jsPsych.plugins.parameterType.STRING],
				default: undefined,
				no_function: false,
				description: ''
			},
			coordinates: {
				type: [jsPsych.plugins.parameterType.INT],
				array: true,
				default: [400, 400],
				no_function: false,
				description: ''
			},
			canvas_size: {
				type: [jsPsych.plugins.parameterType.INT],
				array: true,
				default: [400, 400],
				no_function: false,
				description: ''
			},
			clickNum: {
				type: [jsPsych.plugins.parameterType.STRING],
				default: undefined,
				no_function: false,
				description: ''
			},
			image_size: {
				type: [jsPsych.plugins.parameterType.INT],
				array: true,
				default: [100, 100],
				no_function: false,
				description: ''
			},
			choices: {
				type: [jsPsych.plugins.parameterType.KEYCODE, jsPsych.plugins.parameterType.SELECT],
				options: ['mouse'],
				array: true,
				default: undefined,
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
			csv_directory: {
				type: [jsPsych.plugins.parameterType.STRING],
				default: '',
				no_function: false,
				description: ''
			}
		}
	}

	plugin.trial = function(display_element, trial) {
		$('body').css('background-color', '#6e6e6e')
		var counter = 0;
		// if any trial variables are functions
		// this evaluates the function and replaces
		// it with the output of the function
		trial = jsPsych.pluginAPI.evaluateFunctionParameters(trial);

		// set default values for the parameters
		trial.timing_stim = trial.timing_stim || -1;
		trial.timing_response = trial.timing_response || -1;
		trial.canvas_size = trial.canvas_size || [400, 400];
		trial.image_size = trial.image_size || [100, 100];
		trial.coordinates = trial.coordinates || [100, 100];
		
		if (subject.webcam_used == true){
			/*pause eyetracking*/
			//check if webcam is used
			function webgazerResume(){		
			//put webcam in idle
				if (webgazer_idle == true){
					webgazer.resume(); //begins collecting click data and activates the camera	
					console.log('eyetracker started');
					webgazer_idle = false;
				};
			};
			webgazerResume();
		}
		
		//getting trialNum
		var trialvalue = trial.trialNum;
		
		//checking display window size
		if (trialvalue == 0){
			subject.display_window = [window.innerWidth+"x"+window.innerHeight];
		}
		
		// this array holds handlers from setTimeout calls
		// that need to be cleared if the trial ends early
		var setTimeoutHandlers = [];

		//prepare display stimulus
		var image_size = [200, 200];
		
		//timeout to allow svg to finish (msec)
		var delay = (function() {
    		var timer = 0;
    		return function(callback, ms) {
				clearTimeout (timer);
				timer = setTimeout(callback, ms);
    		};
		})();
		
		//preparing SVG
		var width = 10
		if (loop == 1){
			$('.container-inner').append("<div id='progress'></div>");
			loop = 2;
		}
		var bar = new ProgressBar.Circle('#progress', {
			color: '#ffffff',
			// This has to be the same size as the maximum width to
			// prevent clipping
			strokeWidth: width,
			trailWidth: width,
			easing: 'linear',
			duration: 0,
			from: {
				color: '#ff0000',
				width: 1
			},
			to: {
				color: '##00ff00',
				width: width
			},
			// Set default step function for all animate calls
			step: function(state, circle) {
				circle.path.setAttribute('stroke', state.color);
				circle.path.setAttribute('stroke-width', state.width);
			}
		});

		//stim location
		var square = document.getElementById("progress");
		//get calibration image size
		var css_size = document.getElementById("progress").offsetWidth;
		//note: to get console to print coordinates of svg square.getBoundingClientRect()
		//adust coordinates per trial
		square.style.left = calibration_coordinates[trialvalue][0];
		square.style.top = calibration_coordinates[trialvalue][1];

		//getting stimulus location
		var stim_xy = [Math.floor(trial.canvas_size[0] / 2 - trial.image_size[0] / 2),
					Math.floor(trial.canvas_size[1] / 2 - trial.image_size[1] / 2)
				   ];

		// store response
		var response = {
			rt: -1,
			key: -1
		};

		// function to end trial when it is time
		//delay duration (msec)
		var delay_t = 500;
		var end_trial = function() {
			var visible = vis();
			delay(function(){
				counter = 0;

				//remove elements of progress node
				while (square.firstChild) {
					square.removeChild(square.firstChild);
				};

				//remove progress node if calibration is finished
				if (trialvalue >= (calibration_coordinates.length - 1)){
					document.getElementById("progress").remove();
					};

				//remove event listener (click)
				document.removeEventListener("click", mouseListen, false);

				// kill any remaining setTimeout handlers
				for(var i = 0; i < setTimeoutHandlers.length; i++) {
					clearTimeout(setTimeoutHandlers[i]);
				}
				// kill keyboard listeners
				if(typeof keyboardListener !== 'undefined') {
					jsPsych.pluginAPI.cancelKeyboardResponse(keyboardListener);
				}

				// clear the display
				display_element.html('');
				
				// move on to the next trial
				jsPsych.finishTrial();
			}, delay_t);
		};

		// function to handle responses by the subject
		var after_response = function(info) {
			console.log('keyboard')
			// after a valid response, the stimulus will have the CSS class 'responded'
			// which can be used to provide visual feedback that a response was recorded
			$("#jspsych-calibration-canvas").addClass('responded');

			// only record the first response
			if(response.key == -1) {
				response = info;
			}

			if(trial.response_ends_trial) {
				end_trial();
			}
		};
		
		//mouse listener
		var mouseListen = function(e) {
			if(counter >= trial.clickNum){
				end_trial()
			} else {
				//coordinate listener
				if ($('#progress').is(':hover')) {
					counter = counter + 1;
					//console.log("trialNum:", trialvalue, " clickNum:", counter, " x:", e.screenX + " y:" + e.screenY);
					bar.animate(counter / 20);
				}
			}
		};
		
		// start the response listener
		document.addEventListener("click", mouseListen, false);
		

		// hide image if timing is set
		if(trial.timing_stim > 0) {
			var t1 = setTimeout(function() {
				$('#jspsych-calibration-canvas').css('visibility', 'hidden');
			}, trial.timing_stim);
			setTimeoutHandlers.push(t1);
		}

		// end trial if time limit is set
		if(trial.timing_response > 0) {
			var t2 = setTimeout(function() {
				end_trial();
			}, trial.timing_response);
			setTimeoutHandlers.push(t2);
		}
	};

	return plugin;
})();