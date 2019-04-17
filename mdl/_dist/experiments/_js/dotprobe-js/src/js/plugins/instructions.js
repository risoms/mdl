/****/
jsPsych.plugins.instructions = (function () {

	var plugin = {};

	plugin.info = {
		name: 'instructions',
		description: '',
		parameters: {
			pages: {
				type: [jsPsych.plugins.parameterType.STRING],
				default: undefined,
				array: true,
				no_function: false,
				description: ''
			},
			key_forward: {
				type: [jsPsych.plugins.parameterType.KEYCODE],
				default: 'rightarrow',
				no_function: false,
				description: ''
			},
			key_backward: {
				type: [jsPsych.plugins.parameterType.KEYCODE],
				default: 'leftarrow',
				no_function: false,
				description: ''
			},
			allow_backward: {
				type: [jsPsych.plugins.parameterType.BOOL],
				default: true,
				no_function: false,
				description: ''
			},
			allow_keys: {
				type: [jsPsych.plugins.parameterType.BOOL],
				default: true,
				no_function: false,
				description: ''
			},
			show_clickable_nav: {
				type: [jsPsych.plugins.parameterType.BOOL],
				default: false,
				no_function: false,
				description: ''
			}
		}
	}

	plugin.trial = function (display_element, trial) {

		trial.key_forward = trial.key_forward || 'rightarrow';
		trial.key_backward = trial.key_backward || 'leftarrow';
		trial.allow_backward = (typeof trial.allow_backward === 'undefined') ? true : trial.allow_backward;
		trial.allow_keys = (typeof trial.allow_keys === 'undefined') ? true : trial.allow_keys;
		trial.show_clickable_nav = (typeof trial.show_clickable_nav === 'undefined') ? false : trial.show_clickable_nav;

		// if any trial variables are functions
		// this evaluates the function and replaces
		// it with the output of the function
		trial = jsPsych.pluginAPI.evaluateFunctionParameters(trial);
		
		$('body').css('cursor', 'default'); //return crosshairs
		
		if (subject.webcam_used == true) {
			/*pause eyetracking*/
			//check if webcam is used
			function webgazerPause() {
				//put webcam in idle
				if (webgazer_idle == false) {
					webgazer.pause()
					console.log('eyetracker paused');
					webgazer_idle = true;
				};
			};
			webgazerPause();
		}
		
		//checking display window size
		subject.display_window = [window.innerWidth + "x" + window.innerHeight];
		var current_page = 0;
		var view_history = [];
		var start_time = (new Date()).getTime();
		var last_page_update_time = start_time;

		function show_current_page() {
			display_element.html(trial.pages[current_page]);
			if (trial.show_clickable_nav) {
				var nav_html = "<div class='jspsych-instructions-nav'>";
				if (current_page != 0 && trial.allow_backward) {
					nav_html += "<button id='jspsych-instructions-back' class='jspsych-btn'>&lt; Previous</button>";
				}
				nav_html += "<button id='jspsych-instructions-next' class='jspsych-btn'>Next &gt;</button></div>"
				display_element.append(nav_html);
				if (current_page != 0 && trial.allow_backward) {
					$('#jspsych-instructions-back').on('click', function () {
						clear_button_handlers();
						back();
					});
				}
				$('#jspsych-instructions-next').on('click', function () {
					clear_button_handlers();
					next();
				});
			}
		}

		function clear_button_handlers() {
			$('#jspsych-instructions-next').off('click');
			$('#jspsych-instructions-back').off('click');
		}

		function next() {
			add_current_page_to_view_history()
			current_page++;
			// if done, finish up...
			if (current_page >= trial.pages.length) {
				endTrial();
			} else {
				show_current_page();
			}

		}

		function back() {
			add_current_page_to_view_history()
			current_page--;
			show_current_page();
		}

		function add_current_page_to_view_history() {
			var current_time = (new Date()).getTime();
			var page_view_time = current_time - last_page_update_time;
			view_history.push({
				page_index: current_page,
				viewing_time: page_view_time
			});
			last_page_update_time = current_time;
		}

		function endTrial() {
			var visible = vis();
			if (trial.allow_keys) {
				jsPsych.pluginAPI.cancelKeyboardResponse(keyboard_listener);
			}
			display_element.html('');
			jsPsych.finishTrial();
		}

		var after_response = function (info) {
			keyboard_listener = jsPsych.pluginAPI.getKeyboardResponse({
				callback_function: after_response,
				valid_responses: [trial.key_forward, trial.key_backward],
				rt_method: 'date',
				persist: false,
				allow_held_key: false
			});
			// check if key is forwards or backwards and update page
			if (info.key === trial.key_backward || info.key === jsPsych.pluginAPI.convertKeyCharacterToKeyCode(trial.key_backward)) {
				if (current_page !== 0 && trial.allow_backward) {
					back();
				}
			}
			if (info.key === trial.key_forward || info.key === jsPsych.pluginAPI.convertKeyCharacterToKeyCode(trial.key_forward)) {
				next();
			}
		};

		show_current_page();
		if (trial.allow_keys) {
			var keyboard_listener = jsPsych.pluginAPI.getKeyboardResponse({
				callback_function: after_response,
				valid_responses: [trial.key_forward, trial.key_backward],
				rt_method: 'date',
				persist: false
			});
		}
	};

	return plugin;
})();