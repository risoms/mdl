/**
 * jspsych.js
 * Josh de Leeuw
 *
 * documentation: docs.jspsych.org
 *
 **/
var jsPsych = (function() {

  var core = {};

  //
  // private variables
  //

  // options
  var opts = {};
  // experiment timeline
  var timeline;
  // flow control
  var global_trial_index = 0;
  var current_trial = {};
  // target DOM element
  var DOM_target;
  // time that the experiment began
  var exp_start_time;
  // is the experiment paused?
  var paused = false;
  var waiting = false;
  // done loading?
  var loaded = false;

  // enumerated variables for special parameter types
  core.ALL_KEYS = 'allkeys';
  core.NO_KEYS = 'none';

  //
  // public methods
  //

  core.init = function(options) {

    // reset variables
    timeline = null;
    global_trial_index = 0;
    current_trial = {};
    paused = false;
    waiting = false;
    loaded = false;

    // check if there is a body element on the page
    var default_display_element = $('body');
    if (default_display_element.length === 0) {
      $(document.documentElement).append($('<body>'));
      default_display_element = $('body');
    }

    var defaults = {
      'display_element': default_display_element,
      'on_finish': function(data) {
        return undefined;
      },
      'on_trial_start': function() {
        return undefined;
      },
      'on_trial_finish': function() {
        return undefined;
      },
      'on_data_update': function(data) {
        return undefined;
      },
      'show_progress_bar': false,
      'auto_preload': true,
      'max_load_time': 60000,
      'fullscreen': false,
      'default_iti': 1000
    };

    // override default options if user specifies an option
    opts = $.extend({}, defaults, options);

    // set target
    opts.display_element.append('<div id="jspsych-content"></div>')
    DOM_target = $('#jspsych-content');

    // add CSS class to DOM_target
    opts.display_element.addClass('jspsych-display-element')
    DOM_target.addClass('jspsych-content');

    // create experiment timeline
    timeline = new TimelineNode({
      timeline: opts.timeline
    });

    // create listeners for user browser interaction
    jsPsych.data.createInteractionListeners();

    // start experiment, with or without preloading
    if(opts.auto_preload){
      jsPsych.pluginAPI.autoPreload(timeline, startExperiment);
      if(opts.max_load_time > 0){
        setTimeout(function(){
          if(!loaded){
            loadFail();
          }
        }, opts.max_load_time);
      }
    } else {
      startExperiment();
    }
  };

  core.progress = function() {

    var percent_complete = typeof timeline == 'undefined' ? 0 : timeline.percentComplete();

    var obj = {
      "total_trials": typeof timeline == 'undefined' ? undefined : timeline.length(),
      "current_trial_global": global_trial_index,
      "percent_complete": percent_complete
    };

    return obj;
  };

  core.startTime = function() {
    return exp_start_time;
  };

  core.totalTime = function() {
    if(typeof exp_start_time == 'undefined'){ return 0; }
    return (new Date()).getTime() - exp_start_time.getTime();
  };

  core.getDisplayElement = function() {
    return DOM_target;
  };

  core.finishTrial = function(data) {
    // write the data from the trial
    data = typeof data == 'undefined' ? {} : data;
    jsPsych.data.write(data);

    // get back the data with all of the defaults in
    var trial_data = jsPsych.data.getDataByTrialIndex(global_trial_index);

    // handle callback at plugin level
    if (typeof current_trial.on_finish === 'function') {
      current_trial.on_finish(trial_data);
    }

    // handle callback at whole-experiment level
    opts.on_trial_finish(trial_data);

    // wait for iti
    if (typeof current_trial.timing_post_trial == 'undefined') {
      if (opts.default_iti > 0) {
        setTimeout(nextTrial, opts.default_iti);
      } else {
        nextTrial();
      }
    } else {
      if (current_trial.timing_post_trial > 0) {
        setTimeout(nextTrial, current_trial.timing_post_trial);
      } else {
        nextTrial();
      }
    }
  }

  core.endExperiment = function(end_message) {
    timeline.end_message = end_message;
    timeline.end();
  }

  core.endCurrentTimeline = function() {
    timeline.endActiveNode();
  }

  core.currentTrial = function() {
    return current_trial;
  };

  core.initSettings = function() {
    return opts;
  };

  core.currentTimelineNodeID = function() {
    return timeline.activeID();
  };

  core.timelineVariable = function(varname){
    return timeline.timelineVariable(varname);
  }

  core.addNodeToEndOfTimeline = function(new_timeline, preload_callback){
    timeline.insert(new_timeline);
    if(opts.auto_preload){
      jsPsych.pluginAPI.autoPreload(timeline, preload_callback);
    } else {
      preload_callback();
    }
  }

  core.pauseExperiment = function(){
    paused = true;
  }

  core.resumeExperiment = function(){
    paused = false;
    if(waiting){
      waiting = false;
      nextTrial();
    }
  }

  function TimelineNode(parameters, parent, relativeID) {

    // a unique ID for this node, relative to the parent
    var relative_id;

    // store the parent for this node
    var parent_node;

    // parameters for the trial if the node contains a trial
    var trial_parameters;

    // parameters for nodes that contain timelines
    var timeline_parameters;

    // stores trial information on a node that contains a timeline
    // used for adding new trials
    var node_trial_data;

    // track progress through the node
    var progress = {
      current_location: -1, // where on the timeline (which timelinenode)
      current_variable_set: 0, // which set of variables to use from timeline_variables
      current_repetition: 0, // how many times through the variable set on this run of the node
      current_iteration: 0, // how many times this node has been revisited
      done: false
    }

    // reference to self
    var self = this;

    // recursively get the next trial to run.
    // if this node is a leaf (trial), then return the trial.
    // otherwise, recursively find the next trial in the child timeline.
    this.trial = function() {
      if (typeof timeline_parameters == 'undefined') {
        // returns a clone of the trial_parameters to
        // protect functions.
        return $.extend(true, {}, trial_parameters);
      } else {
        if (progress.current_location >= timeline_parameters.timeline.length) {
          return null;
        } else {
          return timeline_parameters.timeline[progress.current_location].trial();
        }
      }
    }

    this.markCurrentTrialComplete = function() {
      if(typeof timeline_parameters == 'undefined'){
        progress.done = true;
      } else {
        timeline_parameters.timeline[progress.current_location].markCurrentTrialComplete();
      }
    }

    this.nextRepetiton = function() {
      this.setTimelineVariablesOrder();
      progress.current_location = -1;
      progress.current_variable_set = 0;
      progress.current_repetition++;
      for (var i = 0; i < timeline_parameters.timeline.length; i++) {
        timeline_parameters.timeline[i].reset();
      }
    }

    // set the order for going through the timeline variables array
    // TODO: this is where all the sampling options can be implemented
    this.setTimelineVariablesOrder = function() {
      var order = [];
      for(var i=0; i<timeline_parameters.timeline_variables.length; i++){
        order.push(i);
      }

      if(timeline_parameters.randomize_order) {
        order = jsPsych.randomization.shuffle(order);
      }

      progress.order = order;
    }

    // next variable set
    this.nextSet = function() {
      progress.current_location = -1;
      progress.current_variable_set++;
      for (var i = 0; i < timeline_parameters.timeline.length; i++) {
        timeline_parameters.timeline[i].reset();
      }
    }

    // update the current trial node to be completed
    // returns true if the node is complete after advance (all subnodes are also complete)
    // returns false otherwise
    this.advance = function() {

      // first check to see if done
      if (progress.done) {
        return true;
      }

      // if node has not started yet (progress.current_location == -1),
      // then try to start the node.
      if (progress.current_location == -1) {
        // check for conditonal function on nodes with timelines
        if (typeof timeline_parameters != 'undefined') {
          if (typeof timeline_parameters.conditional_function !== 'undefined') {
            var conditional_result = timeline_parameters.conditional_function();
            // if the conditional_function() returns false, then the timeline
            // doesn't run and is marked as complete.
            if (conditional_result == false) {
              progress.done = true;
              return true;
            }
            // if the conditonal_function() returns true, then the node can start
            else {
              progress.current_location = 0;
            }
          }
          // if there is no conditional_function, then the node can start
          else {
            progress.current_location = 0;
          }
        }
        // if the node does not have a timeline, then it can start
        progress.current_location = 0;
        // call advance again on this node now that it is pointing to a new location
        return this.advance();
      }

      // if this node has a timeline, propogate down to the current trial.
      if (typeof timeline_parameters !== 'undefined') {

        var have_node_to_run = false;
        // keep incrementing the location in the timeline until one of the nodes reached is incomplete
        while (progress.current_location < timeline_parameters.timeline.length && have_node_to_run == false) {

          // check to see if the node currently pointed at is done
          var target_complete = timeline_parameters.timeline[progress.current_location].advance();
          if (!target_complete) {
            have_node_to_run = true;
            return false;
          } else {
            progress.current_location++;
          }

        }

        // if we've reached the end of the timeline (which, if the code is here, we have)
        // there are a few steps to see what to do next...

        // first, check the timeline_variables to see if we need to loop through again
        // with a new set of variables
        if (progress.current_variable_set < progress.order.length - 1) {
          // reset the progress of the node to be with the new set
          this.nextSet();
          // then try to advance this node again.
          return this.advance();
        }

        // if we're all done with the timeline_variables, then check to see if there are more repetitions
        else if (progress.current_repetition < timeline_parameters.repetitions - 1) {
          this.nextRepetiton();
          return this.advance();
        }

        // if we're all done with the repetitions, check if there is a loop function.
        else if (typeof timeline_parameters.loop_function !== 'undefined') {
          if (timeline_parameters.loop_function(this.generatedData())) {
            this.reset(); // TODO: fix this probably...
            return parent_node.advance();
          } else {
            progress.done = true;
            return true;
          }
        }

        // no more loops on this timeline, we're done!
        else {
          progress.done = true;
          return true;
        }

      }
    }

    // check the status of the done flag
    this.isComplete = function() {
      return done_flag;
    }

    // getter method for timeline variables
    this.getTimelineVariableValue = function(variable_name){
      if(typeof timeline_parameters == 'undefined'){
        return undefined;
      }
      var v = timeline_parameters.timeline_variables[progress.order[progress.current_variable_set]][variable_name];
      return v;
    }

    // recursive upward search for timeline variables
    this.findTimelineVariable = function(variable_name){
      var v = this.getTimelineVariableValue(variable_name);
      if(typeof v == 'undefined'){
        if(typeof parent_node !== 'undefined'){
          return parent_node.findTimelineVariable(variable_name);
        } else {
          return undefined;
        }
      } else {
        return v;
      }
    }

    // recursive downward search for active trial to extract timeline variable
    this.timelineVariable = function(variable_name){
      if(typeof timeline_parameters == 'undefined'){
        return this.findTimelineVariable(variable_name);
      } else {
        return timeline_parameters.timeline[progress.current_location].timelineVariable(variable_name);
      }
    }

    // recursively get the number of **trials** contained in the timeline
    // assuming that while loops execute exactly once and if conditionals
    // always run
    this.length = function() {
      var length = 0;
      if (typeof timeline_parameters !== 'undefined') {
        for (var i = 0; i < timeline_parameters.timeline.length; i++) {
          length += timeline_parameters.timeline[i].length();
        }
      } else {
        return 1;
      }
      return length;
    }

    // return the percentage of trials completed, grouped at the first child level
    // counts a set of trials as complete when the child node is done
    this.percentComplete = function() {
      var total_trials = this.length();
      var completed_trials = 0;
      for (var i = 0; i < timeline.length; i++) {
        if (timeline[i].isComplete()) {
          completed_trials += timeline[i].length();
        }
      }
      return (completed_trials / total_trials * 100)
    }

    // resets the node and all subnodes to original state
    // but increments the current_iteration counter
    this.reset = function() {
      progress.current_location = -1;
      progress.current_repetition = 0;
      progress.current_variable_set = 0;
      progress.current_iteration++;
      progress.done = false;
      if (typeof timeline_parameters != 'undefined') {
        for (var i = 0; i < timeline_parameters.timeline.length; i++) {
          timeline_parameters.timeline[i].reset();
        }
      }

    }

    // mark this node as finished
    this.end = function() {
      progress.done = true;
    }

    // recursively end whatever sub-node is running the current trial
    this.endActiveNode = function() {
      if (timeline.length == 0) {
        this.end();
        parent_node.end();
      } else {
        timeline[current_location].endActiveNode();
      }
    }

    // get a unique ID associated with this node
    // the ID reflects the current iteration through this node.
    this.ID = function() {
      var id = "";
      if (typeof parent_node == 'undefined') {
        return "0." + progress.current_iteration;
      } else {
        id += parent_node.ID() + "-";
        id += relative_id + "." + progress.current_iteration;
        return id;
      }
    }

    // get the ID of the active trial
    this.activeID = function() {
      if (typeof timeline_parameters == 'undefined') {
        return this.ID();
      } else {
        return timeline_parameters.timeline[progress.current_location].activeID();
      }
    }

    // get all the data generated within this node
    this.generatedData = function() {
      return jsPsych.data.getDataByTimelineNode(this.ID());
    }

    // get all the trials of a particular type
    this.trialsOfType = function(type) {
      if (typeof timeline_parameters == 'undefined'){
        if (trial_parameters.type == type) {
          return trial_parameters;
        } else {
          return [];
        }
      } else {
        var trials = [];
        for (var i = 0; i < timeline_parameters.timeline.length; i++) {
          var t = timeline_parameters.timeline[i].trialsOfType(type);
          trials = trials.concat(t);
        }
        return trials;
      }
    }

    // add new trials to end of this timeline
    this.insert = function(parameters){
      if(typeof timeline_parameters == 'undefined'){
        console.error('Cannot add new trials to a trial-level node.');
      } else {
        timeline_parameters.timeline.push(
          new TimelineNode($.extend(true, {}, node_trial_data, parameters), self, timeline_parameters.timeline.length)
        );
      }
    }

    // constructor
    var _construct = function() {

      // store a link to the parent of this node
      parent_node = parent;

      // create the ID for this node
      if (typeof parent == 'undefined') {
        relative_id = 0;
      } else {
        relative_id = relativeID;
      }

      // check if there is a timeline parameter
      // if there is, then this node has its own timeline
      if (typeof parameters.timeline !== 'undefined') {

        // create timeline properties
        timeline_parameters = {
          timeline: [],
          loop_function: parameters.loop_function,
          conditional_function: parameters.conditional_function,
          randomize_order: typeof parameters.randomize_order == 'undefined' ? false : parameters.randomize_order,
          repetitions: typeof parameters.repetitions == 'undefined' ? 1 : parameters.repetitions,
          timeline_variables: typeof parameters.timeline_variables == 'undefined' ? [{}] : parameters.timeline_variables
        };

        self.setTimelineVariablesOrder();

        // extract all of the node level data and parameters
        var node_data = $.extend(true, {}, parameters);
        delete node_data.timeline;
        delete node_data.conditional_function;
        delete node_data.loop_function;
        delete node_data.randomize_order;
        delete node_data.repetitions;
        delete node_data.timeline_variables;
        node_trial_data = node_data; // store for later...

        // create a TimelineNode for each element in the timeline
        for (var i = 0; i < parameters.timeline.length; i++) {
          timeline_parameters.timeline.push(new TimelineNode($.extend(true, {}, node_data, parameters.timeline[i]), self, i));
        }

      }
      // if there is no timeline parameter, then this node is a trial node
      else {
        // check to see if a valid trial type is defined
        var trial_type = parameters.type;
        if (typeof trial_type == 'undefined') {
          console.error('Trial level node is missing the "type" parameter. The parameters for the node are: ' + JSON.stringify(parameters));
        } else if (typeof jsPsych.plugins[trial_type] == 'undefined') {
          console.error('No plugin loaded for trials of type "' + trial_type + '"');
        }
        // create a deep copy of the parameters for the trial
        trial_parameters = $.extend(true, {}, parameters);
      }

    }();
  }

  function startExperiment() {

    loaded = true;

    var fullscreen = opts.fullscreen;

    // fullscreen setup
    if (fullscreen) {
      // check if keys are allowed in fullscreen mode
      var keyboardNotAllowed = typeof Element !== 'undefined' && 'ALLOW_KEYBOARD_INPUT' in Element;
      if (keyboardNotAllowed) {
        go();
      } else {
        DOM_target.append(
		"<div id=instructions>" +
			"<p>Before beginning the experiment please be sure to close all other tabs and programs. This will allow the task to progress successfully.</p>" +
			'<p>The experiment will launch in fullscreen mode when you click the button below.</p>'+
			'<button id="jspsych-fullscreen-btn" class="jspsych-btn">Launch Experiment</button>'+
			'</div>');
        $('#jspsych-fullscreen-btn').on('click', function() {
			var element = document.documentElement;
			if (element.requestFullscreen) {
				element.requestFullscreen();
			} else if (element.mozRequestFullScreen) {
				element.mozRequestFullScreen();
			} else if (element.webkitRequestFullscreen) {
				element.webkitRequestFullscreen();
			} else if (element.webkitRequestFullScreen) {
				element.webkitRequestFullScreen();
			} else if (element.msRequestFullscreen) {
				element.msRequestFullscreen();
			}
			$('#jspsych-fullscreen-btn').off('click');
			DOM_target.html('');
			setTimeout(go, 1000);
        });
      }
    } else {
      go();
    }

    function go() {
      // show progress bar if requested
      if (opts.show_progress_bar === true) {
        drawProgressBar();
      }

      // record the start time
      exp_start_time = new Date();

      // begin!
      timeline.advance();
      doTrial(timeline.trial());
    }
  }

  function finishExperiment() {
    opts.on_finish(jsPsych.data.getData());

    if(typeof timeline.end_message !== 'undefined'){
      DOM_target.html(timeline.end_message);
    }

    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen();
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    }

  }

  function nextTrial() {
    // if experiment is paused, don't do anything.
    if(paused) {
      waiting = true;
      return;
    }

    global_trial_index++;

    // advance timeline
    timeline.markCurrentTrialComplete();
    var complete = timeline.advance();

    // update progress bar if shown
    if (opts.show_progress_bar === true) {
      updateProgressBar();
    }

    // check if experiment is over
    if (complete) {
      finishExperiment();
      return;
    }

    doTrial(timeline.trial());
  }

  function doTrial(trial) {

    current_trial = trial;

    // call experiment wide callback
    opts.on_trial_start();

    // check if trial has it's own display element
    var display_element = DOM_target;
    if(typeof trial.display_element !== 'undefined'){
      display_element = trial.display_element;
    }

    // execute trial method
    jsPsych.plugins[trial.type].trial(display_element, trial);
  }

  function loadFail(){
    DOM_target.html('<p>The experiment failed to load.</p>');
  }

  function drawProgressBar() {
    $('.jspsych-display-element').prepend(
      '<div id="jspsych-progressbar-container">'+
      '<span>Completion Progress</span>'+
      '<div id="jspsych-progressbar-outer">'+
        '<div id="jspsych-progressbar-inner"></div>'+
      '</div></div>'
    );
    $('.jspsych-content').wrap(
      '<div class="jspsych-content-wrapper"></div>'
    );
  }

  function updateProgressBar() {
    var progress = jsPsych.progress();

    $('#jspsych-progressbar-inner').css('width', progress.percent_complete + "%");
  }

  return core;
})();

jsPsych.plugins = {

  // enumerate possible parameter types for plugins
  parameterType: {
    BOOL: 0,
    STRING: 1,
    INT: 2,
    FLOAT: 3,
    FUNCTION: 4,
    KEYCODE: 5,
    SELECT: 6
  }

};

jsPsych.data = (function() {

  var module = {};

  // data storage object
  var allData = [];

  // browser interaction event data
  var interactionData = [];

  // data properties for all trials
  var dataProperties = {};

  // ignored data fields
  var ignoredProperties = [];

  // cache the query_string
  var query_string;

  module.getData = function() {
    return $.extend(true, [], allData); // deep clone
  };

  module.getforServer = function() {
	eye_data = _.clone(sample_array);//prepare eye data
	prac_data = jsPsych.data.getTrialsOfType("dotprobe-practice");//prepare practice data
	behav_data = jsPsych.data.getTrialsOfType("dotprobe-task");//prepare task data
	merged_data = merge_array(prac_data,behav_data,eye_data)//merge data
	return merged_data
  };

  module.getInteractionData = function() {
    return $.extend(true, [], interactionData);
  }

  module.write = function(data_object) {

    var progress = jsPsych.progress();
    var trial = jsPsych.currentTrial();

    //var trial_opt_data = typeof trial.data == 'function' ? trial.data() : trial.data;

    var default_data = {
      'trial_type': trial.type,
      'trial_index': progress.current_trial_global,
      'time_elapsed': jsPsych.totalTime(),
      'internal_node_id': jsPsych.currentTimelineNodeID()
    };

    var ext_data_object = $.extend({}, data_object, trial.data, default_data, dataProperties);

    for(var i in ignoredProperties){
      delete ext_data_object[ignoredProperties[i]];
    }

    allData.push(ext_data_object);

    var initSettings = jsPsych.initSettings();
    initSettings.on_data_update(ext_data_object);
  };

  module.addProperties = function(properties) {

    // first, add the properties to all data that's already stored
    for (var i = 0; i < allData.length; i++) {
      for (var key in properties) {
        allData[i][key] = properties[key];
      }
    }

    // now add to list so that it gets appended to all future data
    dataProperties = $.extend({}, dataProperties, properties);
  };

  module.ignore = function(properties) {

    // first, remove the properties from all data that's already stored
    for (var i = 0; i < allData.length; i++) {
      for (var j in properties) {
        delete allData[i][properties[j]];
      }
    }

    // now add to list so that it gets appended to all future data
    ignoredProperties = ignoredProperties.concat(properties);
  };

  module.addDataToLastTrial = function(data) {
    if (allData.length == 0) {
      throw new Error("Cannot add data to last trial - no data recorded so far");
    }
    allData[allData.length - 1] = $.extend({}, allData[allData.length - 1], data);
  }

  module.dataAsCSV = function() {
    var dataObj = module.getData();
    return JSON2CSV(dataObj);
  };
	
  module.forServer = function() {
    var dataObj = module.getforServer();
    return JSON2CSV(dataObj);
  };

  module.dataAsJSON = function() {
    var dataObj = module.getData();
    return JSON.stringify(dataObj);
  };

  module.localSave = function(filename, format) {

    var data_string;

    if (format == 'JSON' || format == 'json') {
      data_string = JSON.stringify(module.getData());
    } else if (format == 'CSV' || format == 'csv') {
      data_string = module.dataAsCSV();
    } else {
      throw new Error('invalid format specified for jsPsych.data.localSave');
    }

    saveTextToFile(data_string, filename);
  };

  module.getTrialsOfType = function(trial_type) {
    var data = module.getData();

    data = flatten(data);

    var trials = [];
    for (var i = 0; i < data.length; i++) {
      if (data[i].trial_type == trial_type) {
        trials.push(data[i]);
      }
    }

    return trials;
  };

  module.getDataByTimelineNode = function(node_id) {
    var data = module.getData();

    data = flatten(data);

    var trials = [];
    for (var i = 0; i < data.length; i++) {
      if (data[i].internal_node_id.slice(0, node_id.length) === node_id) {
        trials.push(data[i]);
      }
    }

    return trials;
  };

  module.getLastTrialData = function() {
    if (allData.length == 0) {
      return {};
    }
    return allData[allData.length - 1];
  };

  module.getDataByTrialIndex = function(trial_index) {
    for (var i = 0; i < allData.length; i++) {
      if (allData[i].trial_index == trial_index) {
        return allData[i];
      }
    }
    return undefined;
  }

  module.getLastTimelineData = function() {
    var lasttrial = module.getLastTrialData();
    var node_id = lasttrial.internal_node_id;
    if (typeof node_id === 'undefined') {
      return [];
    } else {
      var parent_node_id = node_id.substr(0,node_id.lastIndexOf('-'));
      var lastnodedata = module.getDataByTimelineNode(parent_node_id);
      return lastnodedata;
    }
  }

  module.displayData = function(format) {
    format = (typeof format === 'undefined') ? "json" : format.toLowerCase();
    if (format != "json" && format != "csv") {
      console.log('Invalid format declared for displayData function. Using json as default.');
      format = "json";
    }

    var data_string;

    if (format == 'json') {
      data_string = JSON.stringify(module.getData(), undefined, 1);
    } else {
      data_string = module.dataAsCSV();
    }

    var display_element = jsPsych.getDisplayElement();

    display_element.append($('<pre id="jspsych-data-display"></pre>'));

    $('#jspsych-data-display').text(data_string);
  };

  module.urlVariables = function() {
    if(typeof query_string == 'undefined'){
      query_string = getQueryString();
    }
    return query_string;
  }

  module.getURLVariable = function(whichvar){
    if(typeof query_string == 'undefined'){
      query_string = getQueryString();
    }
    return query_string[whichvar];
  }

  module.createInteractionListeners = function(){
    // blur event capture
    window.addEventListener('blur', function(){
      interactionData.push({
        event: 'blur',
        trial: jsPsych.progress().current_trial_global,
        time: jsPsych.totalTime()
      });
    });

    // focus event capture
    window.addEventListener('focus', function(){
      interactionData.push({
        event: 'focus',
        trial: jsPsych.progress().current_trial_global,
        time: jsPsych.totalTime()
      });
    });

    // fullscreen change capture
    function fullscreenchange() {
    	var type = (document.isFullScreen || document.webkitIsFullScreen || document.mozIsFullScreen) ? 'fullscreenenter' : 'fullscreenexit';
    	interactionData.push({
    		event: type,
    		trial: jsPsych.progress().current_trial_global,
    		time: jsPsych.totalTime()
    	});
    }

    document.addEventListener('fullscreenchange', fullscreenchange);
    document.addEventListener('mozfullscreenchange', fullscreenchange);
    document.addEventListener('webkitfullscreenchange', fullscreenchange);
  }

  // private function to save text file on local drive

  function saveTextToFile(textstr, filename) {
    var blobToSave = new Blob([textstr], {
      type: 'text/plain'
    });
    var blobURL = "";
    if (typeof window.webkitURL !== 'undefined') {
      blobURL = window.webkitURL.createObjectURL(blobToSave);
    } else {
      blobURL = window.URL.createObjectURL(blobToSave);
    }

    var display_element = jsPsych.getDisplayElement();

    display_element.append($('<a>', {
      id: 'jspsych-download-as-text-link',
      href: blobURL,
      css: {
        display: 'none'
      },
      download: filename,
      html: 'download file'
    }));
    $('#jspsych-download-as-text-link')[0].click();
  }

  //
  // A few helper functions to handle data format conversion
  //

  // this function based on code suggested by StackOverflow users:
  // http://stackoverflow.com/users/64741/zachary
  // http://stackoverflow.com/users/317/joseph-sturtevant

  function JSON2CSV(objArray) {
    var array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
    var line = '';
    var result = '';
    var columns = [];

    var i = 0;
    for (var j = 0; j < array.length; j++) {
      for (var key in array[j]) {
        var keyString = key + "";
        keyString = '"' + keyString.replace(/"/g, '""') + '",';
        if ($.inArray(key, columns) == -1) {
          columns[i] = key;
          line += keyString;
          i++;
        }
      }
    }

    line = line.slice(0, -1);
    result += line + '\r\n';

    for (var i = 0; i < array.length; i++) {
      var line = '';
      for (var j = 0; j < columns.length; j++) {
        var value = (typeof array[i][columns[j]] === 'undefined') ? '' : array[i][columns[j]];
        var valueString = value + "";
        line += '"' + valueString.replace(/"/g, '""') + '",';
      }

      line = line.slice(0, -1);
      result += line + '\r\n';
    }

    return result;
  }

  // this function is modified from StackOverflow:
  // http://stackoverflow.com/posts/3855394

  function getQueryString() {
    var a = window.location.search.substr(1).split('&');
    if (a == "") return {};
    var b = {};
    for (var i = 0; i < a.length; ++i)
    {
        var p=a[i].split('=', 2);
        if (p.length == 1)
            b[p[0]] = "";
        else
            b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
    }
    return b;
  }

  return module;

})();

jsPsych.turk = (function() {

  var module = {};

  // core.turkInfo gets information relevant to mechanical turk experiments. returns an object
  // containing the workerID, assignmentID, and hitID, and whether or not the HIT is in
  // preview mode, meaning that they haven't accepted the HIT yet.
  module.turkInfo = function() {

    var turk = {};

    var param = function(url, name) {
      name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
      var regexS = "[\\?&]" + name + "=([^&#]*)";
      var regex = new RegExp(regexS);
      var results = regex.exec(url);
      return (results == null) ? "" : results[1];
    };

    var src = param(window.location.href, "assignmentId") ? window.location.href : document.referrer;

    var keys = ["assignmentId", "hitId", "workerId", "turkSubmitTo"];
    keys.map(

      function(key) {
        turk[key] = unescape(param(src, key));
      });

    turk.previewMode = (turk.assignmentId == "ASSIGNMENT_ID_NOT_AVAILABLE");

    turk.outsideTurk = (!turk.previewMode && turk.hitId === "" && turk.assignmentId == "" && turk.workerId == "")

    turk_info = turk;

    return turk;

  };

  // core.submitToTurk will submit a MechanicalTurk ExternalHIT type
  module.submitToTurk = function(data) {

    var turkInfo = jsPsych.turk.turkInfo();
    var assignmentId = turkInfo.assignmentId;
    var turkSubmitTo = turkInfo.turkSubmitTo;

    if (!assignmentId || !turkSubmitTo) return;

    var dataString = [];

    for (var key in data) {

      if (data.hasOwnProperty(key)) {
        dataString.push(key + "=" + escape(data[key]));
      }
    }

    dataString.push("assignmentId=" + assignmentId);

    var url = turkSubmitTo + "/mturk/externalSubmit?" + dataString.join("&");

    window.location.href = url;
  };

  return module;

})();

jsPsych.randomization = (function() {

  var module = {};

  module.repeat = function(array, repetitions, unpack) {

    var arr_isArray = Array.isArray(array);
    var rep_isArray = Array.isArray(repetitions);

    // if array is not an array, then we just repeat the item
    if (!arr_isArray) {
      if (!rep_isArray) {
        array = [array];
        repetitions = [repetitions];
      } else {
        repetitions = [repetitions[0]];
        console.log('Unclear parameters given to randomization.repeat. Multiple set sizes specified, but only one item exists to sample. Proceeding using the first set size.');
      }
    } else {
      if (!rep_isArray) {
        var reps = [];
        for (var i = 0; i < array.length; i++) {
          reps.push(repetitions);
        }
        repetitions = reps;
      } else {
        if (array.length != repetitions.length) {
          console.warning('Unclear parameters given to randomization.repeat. Items and repetitions are unequal lengths. Behavior may not be as expected.');
          // throw warning if repetitions is too short, use first rep ONLY.
          if (repetitions.length < array.length) {
            var reps = [];
            for (var i = 0; i < array.length; i++) {
              reps.push(repetitions);
            }
            repetitions = reps;
          } else {
            // throw warning if too long, and then use the first N
            repetitions = repetions.slice(0, array.length);
          }
        }
      }
    }

    // should be clear at this point to assume that array and repetitions are arrays with == length
    var allsamples = [];
    for (var i = 0; i < array.length; i++) {
      for (var j = 0; j < repetitions[i]; j++) {
        if(array[i] == null || typeof array[i] != 'object'){
          allsamples.push(array[i]);
        } else {
          allsamples.push($.extend(true, {}, array[i]));
        }

      }
    }

    var out = shuffle(allsamples);

    if (unpack) {
      out = unpackArray(out);
    }

    return out;
  }

  module.shuffle = function(arr) {
    return shuffle(arr);
  }

  module.shuffleNoRepeats = function(arr, equalityTest) {
    // define a default equalityTest
    if (typeof equalityTest == 'undefined') {
      equalityTest = function(a, b) {
        if (a === b) {
          return true;
        } else {
          return false;
        }
      }
    }

    var random_shuffle = shuffle(arr);
    for (var i = 0; i < random_shuffle.length - 2; i++) {
      if (equalityTest(random_shuffle[i], random_shuffle[i + 1])) {
        // neighbors are equal, pick a new random neighbor to swap (not the first or last element, to avoid edge cases)
        var random_pick = Math.floor(Math.random() * (random_shuffle.length - 2)) + 1;
        // test to make sure the new neighbor isn't equal to the old one
        while (
          equalityTest(random_shuffle[i + 1], random_shuffle[random_pick]) ||
          (equalityTest(random_shuffle[i + 1], random_shuffle[random_pick + 1]) || equalityTest(random_shuffle[i + 1], random_shuffle[random_pick - 1]))
        ) {
          random_pick = Math.floor(Math.random() * (random_shuffle.length - 2)) + 1;
        }
        var new_neighbor = random_shuffle[random_pick];
        random_shuffle[random_pick] = random_shuffle[i + 1];
        random_shuffle[i + 1] = new_neighbor;
      }
    }

    return random_shuffle;
  }

  module.sample = function(arr, size, withReplacement) {
    if (withReplacement == false) {
      if (size > arr.length) {
        console.error("jsPsych.randomization.sample cannot take a sample " +
          "larger than the size of the set of items to sample from when " +
          "sampling without replacement.");
      }
    }
    var samp = [];
    var shuff_arr = shuffle(arr);
    for (var i = 0; i < size; i++) {
      if (!withReplacement) {
        samp.push(shuff_arr.pop());
      } else {
        samp.push(shuff_arr[Math.floor(Math.random() * shuff_arr.length)]);
      }
    }
    return samp;
  }

  module.factorial = function(factors, repetitions, unpack) {

    var factorNames = Object.keys(factors);

    var factor_combinations = [];

    for (var i = 0; i < factors[factorNames[0]].length; i++) {
      factor_combinations.push({});
      factor_combinations[i][factorNames[0]] = factors[factorNames[0]][i];
    }

    for (var i = 1; i < factorNames.length; i++) {
      var toAdd = factors[factorNames[i]];
      var n = factor_combinations.length;
      for (var j = 0; j < n; j++) {
        var base = factor_combinations[j];
        for (var k = 0; k < toAdd.length; k++) {
          var newpiece = {};
          newpiece[factorNames[i]] = toAdd[k];
          factor_combinations.push($.extend({}, base, newpiece));
        }
      }
      factor_combinations.splice(0, n);
    }

    repetitions = (typeof repetitions === 'undefined') ? 1 : repetitions;
    var with_repetitions = module.repeat(factor_combinations, repetitions, unpack);

    return with_repetitions;
  }

  module.randomID = function(length){
    var result = '';
    var length = (typeof length == 'undefined') ? 32 : length;
    var chars = '0123456789abcdefghjklmnopqrstuvwxyz';
    for(var i = 0; i<length; i++){
      result += chars[Math.floor(Math.random() * chars.length)];
    }
    return result;
  }

  function unpackArray(array) {

    var out = {};

    for (var i = 0; i < array.length; i++) {
      var keys = Object.keys(array[i]);
      for (var k = 0; k < keys.length; k++) {
        if (typeof out[keys[k]] === 'undefined') {
          out[keys[k]] = [];
        }
        out[keys[k]].push(array[i][keys[k]]);
      }
    }

    return out;
  }

  function shuffle(array) {
    var copy_array = array.slice(0);
    var m = copy_array.length,
      t, i;

    // While there remain elements to shuffle…
    while (m) {

      // Pick a remaining element…
      i = Math.floor(Math.random() * m--);

      // And swap it with the current element.
      t = copy_array[m];
      copy_array[m] = copy_array[i];
      copy_array[i] = t;
    }

    return copy_array;
  }

  return module;

})();

jsPsych.pluginAPI = (function() {

  var module = {};

  // keyboard listeners //
  var keyboard_listeners = [];

  var held_keys = [];

  module.getKeyboardResponse = function(parameters) {
    //parameters are: callback_function, valid_responses, rt_method, persist, audio_context, audio_context_start_time, allow_held_key?

    parameters.rt_method = (typeof parameters.rt_method === 'undefined') ? 'date' : parameters.rt_method;
    if (parameters.rt_method != 'date' && parameters.rt_method != 'performance' && parameters.rt_method != 'audio') {
      console.log('Invalid RT method specified in getKeyboardResponse. Defaulting to "date" method.');
      parameters.rt_method = 'date';
    }

    var start_time;
    if (parameters.rt_method == 'date') {
      start_time = (new Date()).getTime();
    } else if (parameters.rt_method == 'performance') {
      start_time = performance.now();
    } else if (parameters.rt_method == 'audio') {
      start_time = parameters.audio_context_start_time;
    }

    var listener_id;

    var listener_function = function(e) {

      var key_time;
      if (parameters.rt_method == 'date') {
        key_time = (new Date()).getTime();
      } else if (parameters.rt_method == 'performance') {
        key_time = performance.now();
      } else if (parameters.rt_method == 'audio') {
        key_time = parameters.audio_context.currentTime
      }

      var valid_response = false;
      if (typeof parameters.valid_responses === 'undefined' || parameters.valid_responses == jsPsych.ALL_KEYS) {
        valid_response = true;
      } else {
        if(parameters.valid_responses != jsPsych.NO_KEYS){
          for (var i = 0; i < parameters.valid_responses.length; i++) {
            if (typeof parameters.valid_responses[i] == 'string') {
              if (typeof keylookup[parameters.valid_responses[i]] !== 'undefined') {
                if (e.which == keylookup[parameters.valid_responses[i]]) {
                  valid_response = true;
                }
              } else {
                throw new Error('Invalid key string specified for getKeyboardResponse');
              }
            } else if (e.which == parameters.valid_responses[i]) {
              valid_response = true;
            }
          }
        }
      }
      // check if key was already held down

      if (((typeof parameters.allow_held_key == 'undefined') || !parameters.allow_held_key) && valid_response) {
        for (i in held_keys) {
          if (held_keys[i] == e.which) {
            valid_response = false;
            break;
          }
        }
      }

      if (valid_response) {

        held_keys.push(e.which);

        parameters.callback_function({
          key: e.which,
          rt: key_time - start_time
        });

        if ($.inArray(listener_id, keyboard_listeners) > -1) {

          if (!parameters.persist) {
            // remove keyboard listener
            module.cancelKeyboardResponse(listener_id);
          }
        }

        var after_up = function(up) {

          if (up.which == e.which) {
            $(document).off('keyup', after_up);

            // mark key as released
            held_keys.splice($.inArray(e.which, held_keys), 1);
          }
        };

        $(document).keyup(after_up);
      }
    };

    $(document).keydown(listener_function);

    // create listener id object
    listener_id = {
      type: 'keydown',
      fn: listener_function
    };

    // add this keyboard listener to the list of listeners
    keyboard_listeners.push(listener_id);

    return listener_id;

  };

  module.cancelKeyboardResponse = function(listener) {
    // remove the listener from the doc
    $(document).off(listener.type, listener.fn);

    // remove the listener from the list of listeners
    if ($.inArray(listener, keyboard_listeners) > -1) {
      keyboard_listeners.splice($.inArray(listener, keyboard_listeners), 1);
    }
  };

  module.cancelAllKeyboardResponses = function() {
    for (var i = 0; i < keyboard_listeners.length; i++) {
      $(document).off(keyboard_listeners[i].type, keyboard_listeners[i].fn);
    }
    keyboard_listeners = [];
  };

  module.convertKeyCharacterToKeyCode = function(character) {
    var code;
    if (typeof keylookup[character] !== 'undefined') {
      code = keylookup[character];
    }
    return code;
  }

  var keylookup = {
    'backspace': 8,
    'tab': 9,
    'enter': 13,
    'shift': 16,
    'ctrl': 17,
    'alt': 18,
    'pause': 19,
    'capslock': 20,
    'esc': 27,
    'space': 32,
    'spacebar': 32,
    ' ': 32,
    'pageup': 33,
    'pagedown': 34,
    'end': 35,
    'home': 36,
    'leftarrow': 37,
    'uparrow': 38,
    'rightarrow': 39,
    'downarrow': 40,
    'insert': 45,
    'delete': 46,
    '0': 48,
    '1': 49,
    '2': 50,
    '3': 51,
    '4': 52,
    '5': 53,
    '6': 54,
    '7': 55,
    '8': 56,
    '9': 57,
    'a': 65,
    'b': 66,
    'c': 67,
    'd': 68,
    'e': 69,
    'f': 70,
    'g': 71,
    'h': 72,
    'i': 73,
    'j': 74,
    'k': 75,
    'l': 76,
    'm': 77,
    'n': 78,
    'o': 79,
    'p': 80,
    'q': 81,
    'r': 82,
    's': 83,
    't': 84,
    'u': 85,
    'v': 86,
    'w': 87,
    'x': 88,
    'y': 89,
    'z': 90,
    'A': 65,
    'B': 66,
    'C': 67,
    'D': 68,
    'E': 69,
    'F': 70,
    'G': 71,
    'H': 72,
    'I': 73,
    'J': 74,
    'K': 75,
    'L': 76,
    'M': 77,
    'N': 78,
    'O': 79,
    'P': 80,
    'Q': 81,
    'R': 82,
    'S': 83,
    'T': 84,
    'U': 85,
    'V': 86,
    'W': 87,
    'X': 88,
    'Y': 89,
    'Z': 90,
    '0numpad': 96,
    '1numpad': 97,
    '2numpad': 98,
    '3numpad': 99,
    '4numpad': 100,
    '5numpad': 101,
    '6numpad': 102,
    '7numpad': 103,
    '8numpad': 104,
    '9numpad': 105,
    'multiply': 106,
    'plus': 107,
    'minus': 109,
    'decimal': 110,
    'divide': 111,
    'F1': 112,
    'F2': 113,
    'F3': 114,
    'F4': 115,
    'F5': 116,
    'F6': 117,
    'F7': 118,
    'F8': 119,
    'F9': 120,
    'F10': 121,
    'F11': 122,
    'F12': 123,
    '=': 187,
    ',': 188,
    '.': 190,
    '/': 191,
    '`': 192,
    '[': 219,
    '\\': 220,
    ']': 221
  };

  // plugin parameter evaluation //

  module.evaluateFunctionParameters = function(trial, protect) {

    // keys that are always protected
    var always_protected = ['on_finish'];

    protect = (typeof protect === 'undefined') ? [] : protect;

    protect = protect.concat(always_protected);

    var keys = Object.keys(trial);

    for (var i = 0; i < keys.length; i++) {

      var process = true;
      for (var j = 0; j < protect.length; j++) {
        if (protect[j] == keys[i]) {
          process = false;
          break;
        }
      }

      if (typeof trial[keys[i]] == "function" && process) {
        trial[keys[i]] = trial[keys[i]].call();
      }

    }

    return trial;

  };

  // audio //

  // temporary patch for Safari
  if (typeof window !== 'undefined' && window.hasOwnProperty('webkitAudioContext') && !window.hasOwnProperty('AudioContext')) {
    window.AudioContext = webkitAudioContext;
  }
  // end patch

  var context = (typeof window !== 'undefined' && typeof window.AudioContext !== 'undefined') ? new AudioContext() : null;
  var audio_buffers = [];

  module.audioContext = function(){
    return context;
  }

  module.getAudioBuffer = function(audioID) {

    if (audio_buffers[audioID] == 'tmp') {
      console.error('Audio file failed to load in the time alloted.')
      return;
    }

    return audio_buffers[audioID];

  }

  // preloading stimuli //

  var preloads = [];

  module.preloadAudioFiles = function(files, callback_complete, callback_load) {

    files = flatten(files);

    var n_loaded = 0;
    var loadfn = (typeof callback_load === 'undefined') ? function() {} : callback_load;
    var finishfn = (typeof callback_complete === 'undefined') ? function() {} : callback_complete;

    if(files.length==0){
      finishfn();
      return;
    }

    function load_audio_file(source){
      var request = new XMLHttpRequest();
      request.open('GET', source, true);
      request.responseType = 'arraybuffer';
      request.onload = function() {
        context.decodeAudioData(request.response, function(buffer) {
          audio_buffers[source] = buffer;
          n_loaded++;
          loadfn(n_loaded);
          if(n_loaded == files.length) {
            finishfn();
          }
        }, function() {
          console.error('Error loading audio file: ' + bufferID);
        });
      }
      request.send();
    }

    for (var i = 0; i < files.length; i++) {
      var bufferID = files[i];
      if (typeof audio_buffers[bufferID] !== 'undefined') {
        n_loaded++;
        loadfn(n_loaded);
        if(n_loaded == files.length) {
          finishfn();
        }
      }
      audio_buffers[bufferID] = 'tmp';
      load_audio_file(bufferID);
    }

  }

  module.preloadImages = function(images, callback_complete, callback_load) {

    // flatten the images array
    images = flatten(images);

    var n_loaded = 0;
    var loadfn = (typeof callback_load === 'undefined') ? function() {} : callback_load;
    var finishfn = (typeof callback_complete === 'undefined') ? function() {} : callback_complete;

    if(images.length==0){
      finishfn();
      return;
    }

    for (var i = 0; i < images.length; i++) {
      var img = new Image();

      img.onload = function() {
        n_loaded++;
        loadfn(n_loaded);
        if (n_loaded == images.length) {
          finishfn();
        }
      };

      img.onerror = function() {
        n_loaded++;
        loadfn(n_loaded);
        if (n_loaded == images.length) {
          finishfn();
        }
      }

      img.src = images[i];
    }
  };

  module.registerPreload = function(plugin_name, parameter, media_type, conditional_function) {
    if (!(media_type == 'audio' || media_type == 'image')) {
      console.error('Invalid media_type parameter for jsPsych.pluginAPI.registerPreload. Please check the plugin file.');
    }

    var preload = {
      plugin: plugin_name,
      parameter: parameter,
      media_type: media_type,
      conditional_function: conditional_function
    }

    preloads.push(preload);
  }

  module.autoPreload = function(timeline, callback) {
    // list of items to preload
    var images = [];
    var audio = [];

    // construct list
    for (var i = 0; i < preloads.length; i++) {
      var type = preloads[i].plugin;
      var param = preloads[i].parameter;
      var media = preloads[i].media_type;
      var func = preloads[i].conditional_function;
      var trials = timeline.trialsOfType(type);
      for (var j = 0; j < trials.length; j++) {
        if (typeof trials[j][param] !== 'undefined' && typeof trials[j][param] !== 'function') {
          if ( typeof func == 'undefined' || func(trials[j]) ){
            if (media == 'image') {
              images = images.concat(flatten([trials[j][param]]));
            } else if (media == 'audio') {
              audio = audio.concat(flatten([trials[j][param]]));
            }
          }
        }
      }
    }

    // do the preloading
    // first the images, then when the images are complete
    // wait for the audio files to finish
    module.preloadImages(images, function() {
      module.preloadAudioFiles(audio, function() {
        callback();
      });
    });
  }

  return module;
})();

// methods used in multiple modules
function flatten(arr, out) {
  out = (typeof out === 'undefined') ? [] : out;
  for (var i = 0; i < arr.length; i++) {
    if (Array.isArray(arr[i])) {
      flatten(arr[i], out);
    } else {
      out.push(arr[i]);
    }
  }
  return out;
}
