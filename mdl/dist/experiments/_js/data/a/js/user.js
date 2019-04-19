//overlay
function loadingEnd(){
	console.log("loading finished");
	$("#overlay").remove();
};

//graph
function getRandomColor() {//random color generator
	var letters = '0123456789ABCDEF';
	var color = '#';
	for (var i = 0; i < 6; i++) {
		color += letters[Math.floor(Math.random() * 16)];
	}
	return color;
}
//generate graph
//stacked barchart
var temp;
var temp_array;
function generate(){	
	//Wanted mixed object
	temp = [];
	//Store keys, so we do not need to check from temp if key allready exists
	temp_keys = {};
	json_filter = _.filter(json_data, {subject_subsession: 'abc'}); //filter for relevant subession only
	//Loop trough data
	for (var i in json_filter){
		//Check if key is allready stored in object
		if (!temp_keys[json_filter[i]['subject_id']]){
			//Store new key, and save it''s position
			temp_keys[json_filter[i]['subject_id']] = temp.length;
			//Create new array element as new object
			temp.push({
					'name' : json_filter[i]['subject_id'],
					showlegend: true,
					'x': [], //date
					'y': [], //score
					'session': [],
					'type': 'bar',
					'orientation': 'h'
				});
		}
		//Save values into correct position
		temp[temp_keys[json_filter[i]['subject_id']]]['y'].push(
				//json_filter[i]['subject_id']
				json_filter[i]['subject_session']
		);
		temp[temp_keys[json_filter[i]['subject_id']]]['x'].push(
				json_filter[i]['score']
				//json_filter[i]['subject_session']
		);
			//Save values into correct position
		temp[temp_keys[json_filter[i]['subject_id']]]['session'].push(
				json_filter[i]['subject_session']
		);
	};
	temp_array = Object.keys(temp_keys).reverse();
	function PlotlyTimeSeries(){
		layout = {
			autosize: true,
			width: $('.dashboard-main').width(),
			height: $('.dashboard-main').height(),
			"xaxis": {
				'title': "Scores"
			},
			"yaxis": {
				'title': "Session",
        		'categoryorder': "array",
				'categoryarray': temp_array
			},
			legend: {
				bgcolor: '#efefef',
				font: {color: '#666666'}
			},	 
			margin: {l: 40,r: 40,b: 42,t: 40,pad: 4},
			paper_bgcolor: '#f7f7f7',
			plot_bgcolor: '#efefef',
			barmode: 'stack',
			title: 'Subject Scores'
		};
		Plotly.plot('dashboard-data', temp, layout, {displayModeBar: false});
	};
	PlotlyTimeSeries();
}


//generate graph
//plotlines
function generate1(){	
	//Wanted mixed object
	var temp = [];
	//Store keys, so we do not need to check from temp if key allready exists
	var temp_keys = {};
	//Loop trough data
	for (var i in json_data){
		//Check if key is allready stored in object
		if (!temp_keys[json_data[i]['subject_id']]){
			//Store new key, and save it''s position
			temp_keys[json_data[i]['subject_id']] = temp.length;
			//Create new array element as new object
			temp.push({
					'name' : json_data[i]['subject_id'],
					showlegend: false,
					'x': [], //date
					'y': [], //score
					'session': [],
					'type': 'scatter',
					'mode': 'lines', 
					'line': {
						color: getRandomColor(), 
						width: '2'
					}
				});
		}
		//Save values into correct position
		temp[temp_keys[json_data[i]['subject_id']]]['x'].push(
				json_data[i]['end_time']

		);
		temp[temp_keys[json_data[i]['subject_id']]]['y'].push(
				json_data[i]['score']

		);
			//Save values into correct position
		temp[temp_keys[json_data[i]['subject_id']]]['session'].push(
				json_data[i]['subject_session']

		);
	}
	function PlotlyTimeSeries(){
		layout = {
			autosize: true,
			width: $('.dashboard-main').width(),
			height: $('.dashboard-main').height(),
			legend: {
				bgcolor: '#e4e5e7',
				font: {
					color: '#666666'
				}
			},	 
			margin: {l: 30,r: 30,b: 100,t: 50,pad: 4},
			paper_bgcolor: '#e4e5e7',
			plot_bgcolor: '#E5E5E5',
			xaxis1: {
				gridcolor: '#F6F6F6',
				showgrid: true,
				tickfont: {
					color: '#666666'
				},
				title: '',
				titlefont: {
					color: '#666666'
				},
				zerolinecolor: '#F6F6F6'
			},
			yaxis1: {
				gridcolor: '#F6F6F6',
				tickfont: {
					color: '#666666'
				},
				title: '',
				titlefont: {
					color: '#666666'
				},
				zerolinecolor: '#F6F6F6'
			}
		};
		Plotly.plot('dashboard-data', temp, layout, {displayModeBar: true});
	};
	PlotlyTimeSeries();
}

//topbar
function getRecentData() {
	var recentParticipant = (_.uniqBy(cloneJson_data, 'subject_session'))[0]
	recentTicker = "Newest Subject: " + recentParticipant.subject_id +
		", location: " + recentParticipant.location + 
		" (" + recentParticipant.subject_session + "), " + recentParticipant.end_time
	$('#sidebar-subject').text(recentTicker)//most recent subject on top bar
};

//get list of subjects
function getSubjectList(){
	subjectList = [];
	var groupjson = _.uniqBy(cloneJson_data, 'subject_id');
	for (i = 0; i < groupjson.length; i++) {
		subjectList.push(groupjson[i].subject_id);
	};
	//search header
	$(".search-input").autocomplete({
		source: subjectList,
		appendTo: ".search-header",
		autoFill: true,
		select: function (event, ui) {
			var label = ui.item.label;
			var value = ui.item.value;
			var subjson = _.filter(groupjson, {'subject_id': value})[0];
			console.log('autocomplete: '+value)
			console.log('autocomplete')
			console.log(groupjson);
			console.log(subjson);
			getSubjectDetails(value, subjson);
		}
	});
};

//add subject details to dashboard
function getSubjectDetails(subid, group){
	console.log('search updated')
	var newSubjectDetails = [];
	var url = 'https://mdl.psy.utexas.edu/a/r33/?uname='+subid+'&code='+group.code+'&rtco='+group.baseline;
	newSubjectDetails += [
	'<div class="js-item__details">',
		'<div class="id-section">',
			'<div class="id-value">',
				'<div class="id-value-content">'+subid+'</div>',
				'<div class="id-label-content" style="height:10%;font-size: larger;">REDCap ID</div>',
			'</div>',
			'<div class="id-value">',
				'<div class="id-value-content">'+group.baseline+'</div>',
				'<div class="id-label-content" style="height:10%;font-size: larger;">baseline</div>',
			'</div>',
			'<div class="id-value">',
				'<div class="id-value-content">'+group.code+'</div>',
				'<div class="id-label-content" style="height:10%;font-size: larger;">Condition</div>',
			'</div>',
		'</div>',
		'<div class="url-section">',
			'<div class="id-value" style="width: 100%;">',
				'<a href="'+url+'" class="url-value-content">'+url+'</a>',
			'</div>',
		'</div>',
	'</div>'
	].join('');
	$('#subject-url').html(newSubjectDetails.replace('undefined',''))//most recent subject on top bar
};


//recent and old subject list on right-side bar
function getNewList(){
	var newJson = _.uniqBy(cloneJson_data, 'subject_id');
	var newL = newJson.length - 1
	var newElement;
	if (newL < 10){len = newL+1} else {len=10};
	for (i = 0; i < len; i++) {
		var recentSubject = newJson[i];
		subject = recentSubject.subject_id;
		loc=recentSubject.location;
		session=recentSubject.subject_session;
		subsession=recentSubject.subject_subsession;
		score=recentSubject.score;
		date=moment(recentSubject.end_time).format("L");
		time=[moment(recentSubject.start_time).format("hh:mm"),moment(recentSubject.end_time).format("hh:mma")];
		newElement += [
			'<div class="feed-element">',
				'<a class="pull-left">',
					'<div alt="image" class="location-color-'+loc+'"></div>',
				'</a>',
				'<div class="media-body">',
					'<small class="pull-right">'+moment(recentSubject.end_time).fromNow()+'</small>',
					'<strong>'+subject+'</strong> completed session <strong>'+session+'-'+subsession+'</strong> at '+loc+', scoring <strong>'+score+'</strong> points.<br>',
					'<small class="text-muted">'+time[0]+' - '+time[1]+'</small>',
				'</div>',
			'</div>'
		].join('');
	}
	$('#new-subject-container').html(newElement.replace('undefined',''))//most recent subject on top bar
};

//use with defaulting leftside bar as well as recent and old subject list on right-side bar
function getTimeline(){
	var timelineTemplate = [
	'<div class="first-timeline-block lab-item first-timeline-completed" data-animation="slideInUp">',
		'<div class="lab-timeline-img"><span></span></div>',
		'<!-- first-timeline-img -->',
		'<div class="first-timeline-content animated rotateInDownRight" style="position: relative;">',
			'<div class="first-timeline-content-inner">',
				'<span class="first-date-opposite first-date">06/16/2017<br>9:00 - 10:00AM</span>',
				'<h2 class="first-date-header">9999</h2>',
				'<p>session: 1-abc</p>', 
				'<p>score: 4141</p>', 
				'<p>location: lab</p>',
			'</div>',
			'<!-- first-timeline-content-inner -->',
		'</div>',
		'<!-- first-timeline-content -->',
	'</div>'
	].join('');
	for (i = 0; i < 1; i++) {
		$('#timeline').append(timelineTemplate)//most recent subject on top bar
	}
};

//timeline searchbar
var cloneJson_data; //cloned and reversed json_data: most recent data first; use with timeline
function getTimelineSearch(){
	$('#timeline-search').keyup(function () {
		var output, inQuotes;
		var searchField = $(this).val();
		if (searchField === '') {
			$('#timeline').html('');
			return;
		}
		//check if in quotes
		if ((searchField.charAt(0)=="'") || (searchField.charAt(0)=="\"")){
			inQuotes = true;
			quoteChar = searchField.charAt(0)
		} else {
			inQuotes = false;
		}
		var regex = new RegExp(searchField, "i");
		var count = 1;
		$.each(cloneJson_data, function (key, val) {
			var time, date;
			//if ((val.employee_salary.search(regex) != -1) || (val.employee_name.search(regex) != -1)) {//two criteria
			if ((inQuotes) && ((quoteChar+val.subject_id+quoteChar).search(regex) != -1)) {
				//console.log('quotes')
				date=moment(val.end_time).format("L")
				time=[moment(val.start_time).format("hh:mm"),moment(val.end_time).format("hh:mma")];
				output +=[
					'<div class="first-timeline-block '+val.location+'-item first-timeline-completed" data-animation="slideInUp">',
						'<div class="'+val.location+'-timeline-img"> <span></span> </div>',
						'<!-- first-timeline-img -->',
						'<div class="first-timeline-content animated rotateInDownRight" style="position: relative;">',
							'<div class="first-timeline-content-inner">',
								'<span class="first-date-opposite first-date">'+date+'<br>'+time[0]+' - '+time[1]+'</span>',
								'<h2 class="first-date-header">'+val.subject_id+'</h2>',
								'<p>session: '+val.subject_session+'-'+val.subject_subsession+'</p>', 
								'<p>score: '+val.score+'</p>', 
								'<p>location: '+val.location+'</p>',
							'</div>',
							'<!-- first-timeline-content-inner -->',
						'</div>',
						'<!-- first-timeline-content -->',
					'</div>'
				].join('');
			} else if ((val.subject_id.search(regex) != -1) && (!inQuotes)) {
				//console.log('no quotes')
				date=moment(val.end_time).format("L")
				time=[moment(val.start_time).format("hh:mm"),moment(val.end_time).format("hh:mma")];
				output +=[
					'<div class="first-timeline-block '+val.location+'-item first-timeline-completed" data-animation="slideInUp">',
						'<div class="'+val.location+'-timeline-img"> <span></span> </div>',
						'<!-- first-timeline-img -->',
						'<div class="first-timeline-content animated rotateInDownRight" style="position: relative;">',
							'<div class="first-timeline-content-inner">',
								'<span class="first-date-opposite first-date">'+date+'<br>'+time[0]+' - '+time[1]+'</span>',
								'<h2 class="first-date-header">'+val.subject_id+'</h2>',
								'<p>session: '+val.subject_session+'-'+val.subject_subsession+'</p>', 
								'<p>score: '+val.score+'</p>', 
								'<p>location: '+val.location+'</p>',
							'</div>',
							'<!-- first-timeline-content-inner -->',
						'</div>',
						'<!-- first-timeline-content -->',
					'</div>'
				].join('');				
			} else {
				$('#timeline').html('');
			}
		});
		$('#timeline').html(output.replace('undefined',''))//most recent subject on top bar
	});
}

//main searchbar
var cloneJson_data; //cloned and reversed json_data: most recent data first; use with timeline
var tt;
function getMainSearch(){
	$('#main-search').keyup(function () {
		var output = []; 
		var inQuotes;
		var searchField = $(this).val();
		if (searchField === '') {
			$('#timeline').html('');
			return;
		}
		//check if in quotes
		if ((searchField.charAt(0)=="'") || (searchField.charAt(0)=="\"")){
			inQuotes = true;
			quoteChar = searchField.charAt(0)
		} else {
			inQuotes = false;
		}
		var regex = new RegExp(searchField, "i");
		var count = 1;
		$.each(cloneJson_data, function (key, val) {
			var time, date;
			//if ((val.employee_salary.search(regex) != -1) || (val.employee_name.search(regex) != -1)) {//two criteria
			if ((inQuotes) && ((quoteChar+val.subject_id+quoteChar).search(regex) != -1)) {
				//console.log('quotes')
				date=moment(val.end_time).format("L")
				time=[moment(val.start_time).format("hh:mm"),moment(val.end_time).format("hh:mma")];
				output.push({
						date: time[0]+'-'+time[1],
						subject: val.subject_id,
						session: val.subject_session+'-'+val.subject_subsession, 
						score: val.score,
						location: val.location
				});
			} else if ((val.subject_id.search(regex) != -1) && (!inQuotes)) {
				//console.log('no quotes')
				date=moment(val.end_time).format("L")
				time=[moment(val.start_time).format("hh:mm"),moment(val.end_time).format("hh:mma")];
				output.push({
						date: time[0]+'-'+time[1],
						subject: val.subject_id,
						session: val.subject_session+'-'+val.subject_subsession, 
						score: val.score,
						location: val.location
				});				
			} else {
				
			}
		});
		tt = output;
	});
}

function getSearchResults() {
	'use strict';
	var Shuffle = window.shuffle;
	var subjectDetails = function (element) {
	  this.element = element;
	  // Log out events.
	  this.addShuffleEventListeners();
	  this.shuffle = new Shuffle(element, {
		itemSelector: '.js-item',
		sizer: element.querySelector('.my-sizer-element'),
	  });

	  this._activeFilters = [];

	  this.addFilterButtons();
	  this.addSorting();
	  this.addSearchFilter();

	  this.mode = 'exclusive';
	};

	subjectDetails.prototype.toArray = function (arrayLike) {
	  return Array.prototype.slice.call(arrayLike);
	};

	subjectDetails.prototype.toggleMode = function () {
	  if (this.mode === 'additive') {
		this.mode = 'exclusive';
	  } else {
		this.mode = 'additive';
	  }
	};

	/**
	 * Shuffle uses the CustomEvent constructor to dispatch events. You can listen
	 * for them like you normally would (with jQuery for example). The extra event
	 * data is in the `detail` property.
	 */
	subjectDetails.prototype.addShuffleEventListeners = function () {
	  var handler = function (event) {
		console.log('type: %s', event.type, 'detail:', event.detail);
	  };

	  this.element.addEventListener(Shuffle.EventType.LAYOUT, handler, false);
	  this.element.addEventListener(Shuffle.EventType.REMOVED, handler, false);
	};

	subjectDetails.prototype.addFilterButtons = function () {
	  var options = document.querySelector('.filter-options');
	  if (!options) {
		return;
	  }
	  var filterButtons = this.toArray(
		options.children
	  );
	  filterButtons.forEach(function (button) {
		button.addEventListener('click', this._handleFilterClick.bind(this), false);
	  }, this);
	};

	subjectDetails.prototype._handleFilterClick = function (evt) {
	  var btn = evt.currentTarget;
	  var isActive = btn.classList.contains('active');
	  var btnGroup = btn.getAttribute('data-group');

	  // You don't need _both_ of these modes. This is only for the demo.
	  // For this custom 'additive' mode in the demo, clicking on filter buttons
	  // doesn't remove any other filters.
	  if (this.mode === 'additive') {
		// If this button is already active, remove it from the list of filters.
		if (isActive) {
		  this._activeFilters.splice(this._activeFilters.indexOf(btnGroup));
		} else {
		  this._activeFilters.push(btnGroup);
		}

		btn.classList.toggle('active');
		// Filter elements
		this.shuffle.filter(this._activeFilters);

	  // 'exclusive' mode lets only one filter button be active at a time.
	  } else {
		this._removeActiveClassFromChildren(btn.parentNode);
		var filterGroup;
		if (isActive) {
		  btn.classList.remove('active');
		  filterGroup = Shuffle.ALL_ITEMS;
		} else {
		  btn.classList.add('active');
		  filterGroup = btnGroup;
		}
		this.shuffle.filter(filterGroup);
	  }
	};

	subjectDetails.prototype._removeActiveClassFromChildren = function (parent) {
	  var children = parent.children;
	  for (var i = children.length - 1; i >= 0; i--) {
		children[i].classList.remove('active');
	  }
	};

	subjectDetails.prototype.addSorting = function () {
	  var menu = document.querySelector('.sort-options');
	  if (!menu) {
		return;
	  }
	  menu.addEventListener('change', this._handleSortChange.bind(this));
	};

	subjectDetails.prototype._handleSortChange = function (evt) {
	  var value = evt.target.value;
	  var options = {};

	  function sortByDate(element) {
		return element.getAttribute('data-created');
	  }

	  function sortByTitle(element) {
		return element.getAttribute('data-title').toLowerCase();
	  }

	  if (value === 'date-created') {
		options = {
		  reverse: true,
		  by: sortByDate,
		};
	  } else if (value === 'title') {
		options = {
		  by: sortByTitle,
		};
	  }

	  this.shuffle.sort(options);
	};

	// Advanced filtering
	subjectDetails.prototype.addSearchFilter = function () {
	  var searchInput = document.querySelector('.js-shuffle-search');
	  if (!searchInput) {
		return;
	  }
	  searchInput.addEventListener('keyup', this._handleSearchKeyup.bind(this));
	};

	/**
	 * Filter the shuffle instance by items with a title that matches the search input.
	 * @param {Event} evt Event object.
	 */
	subjectDetails.prototype._handleSearchKeyup = function (evt) {
	  var searchText = evt.target.value.toLowerCase();
	  this.shuffle.filter(function (element, shuffle) {
		// If there is a current filter applied, ignore elements that don't match it.
		if (shuffle.group !== Shuffle.ALL_ITEMS) {
		  // Get the item's groups.
		  var groups = JSON.parse(element.getAttribute('data-groups'));
		  var isElementInCurrentGroup = groups.indexOf(shuffle.group) !== -1;
		  // Only search elements in the current group
		  if (!isElementInCurrentGroup) {
			return false;
		  }
		}
		var titleElement = element.querySelector('.picture-item__title');
		var titleText = titleElement.textContent.toLowerCase().trim();
		return titleText.indexOf(searchText) !== -1;
	  });
	};
	document.addEventListener('DOMContentLoaded', function () {
	  window.demo = new subjectDetails(document.getElementById('grid'));
	});
};

//file download
function beforeRequest(arguments) {
	arguments.ajaxSettings.contentType = "application/x-www-form-urlencoded";
};
var fileExplorer;
function getDownload(){
	$("#fileExplorer").ejFileExplorer({
		isResponsive: true,
		enableResize: false,
		width:"100%",
		height: $('.dashboard-main').height() - 2,
		minHeight: "400px",
		toolsList: ["layout","navigation", "addressBar", "editing", "copyPaste", "getProperties", "searchBar"],
		tools: {
			layout: ["Layout"],
			navigation: ["Back", "Forward", "Upward"],
			addressBar: ["Addressbar"],
			editing: ["Refresh", "Rename", "Download"],
			getProperties: ["Details"],
			copyPaste: ["Copy"],
			searchBar: ["Searchbar"]
		},
		contextMenuSettings:{
			items:{
				cwd: ["Refresh", "Paste","|", "SortBy", "|", "NewFolder", "|", "Getinfo", "View"],//rightclick folder
				files: ["Open", "Download",  "|", "Copy", "Paste", "Rename", "|", "OpenFolderLocation", "Getinfo"]//rightclick item
			},
			customMenuFields: [{
				id: "View",
				text: "View",
				child: [{
					id: "Tile",
					text: "Tile",
					action: "onlayout"
				},{
					id: "Grid",
					text: "Grid",
					action: "onlayout"
				},{
					id: "LargeIcons",
					text: "Large icons",
					action: "onlayout"
				}]
			}]
		},
		layout: "tile",
		fileTypes: "*.json, *.csv, *.xls, *.pdf, *.png, *.gif, *.jpg, *.jpeg, *.doc, *.docx",
		path: window.location.origin + '/a/r33/src/csv/data/', 
		ajaxAction: window.location.origin + '/a/r33/data/a/php/FileExplorer/',
		beforeAjaxRequest: "beforeRequest",
		ajaxDataType: "jsonp",
		layoutChange: "onLayoutChange",
		menuOpen: "onMenuOpen",
		allowMultiSelection: true
	});
	fe = $("#fileExplorer").data("ejFileExplorer");
	$('.e-switchView').hide(); //hide annoying footer info
	return fe;
}

//control calendar
var clndr; var popoverElement;
function popoverTemplate(eventColor,backgroundColor,LocationInfo){
	popTemplate = [
		'<div class="popover popover-'+LocationInfo+'" data-toggle="popover" data-trigger="focus" style="max-width:600px;" >',
			'<div class="arrow"></div>',
			'<div class="popover-header" id="eventClick">',
				'<h3 class="popover-title" id="event-click" style="background-color: '+eventColor+'"></h3>',
			'</div>',
			'<div class="popover-content" style="background-color: '+backgroundColor+'"></div>',
		'</div>'].join('');
	return popTemplate
}

var eventColor,session,headerLabels;
function calendarData(){
	console.log(gcalList)
	if (window.outerWidth < 800){
		headerLabels = {
			left: 'prev, agendaDay',
			center: 'title',
			right: 'month, next'
		}
	} else {
		headerLabels = {
			left: 'today,prev,next',
			center: 'title',
			right: 'month,agendaWeek,agendaDay,listMonth'
		}
	}
	if((typeof json_data !== "undefined") && (typeof gcalList !== "undefined")){
		cloneJson_data = (_.clone(json_data)).reverse()
		getRecentData()//get most recent participant data
		getTimeline()//get timeline
		getTimelineSearch()//get timeline search
		getNewList() //getOldList();//right-side bar
		getSubjectList() //get subject list for getMainSearch()
		getMainSearch() //search tab
		generate() //data view
		clndr = $('#calendar').fullCalendar({
			header: headerLabels,
			allDaySlot: false,
			views: {
				month: {editable: false},
				week: {editable: false},
				agendaDay: {
					editable: false,
					titleFormat: 'MMM DD, YYYY'
				}
			},			
			selectable: true,
    		selectHelper: false,
			theme: true,
			themeButtonIcons: {prev: 'left-single-arrow', next: 'right-single-arrow'},
			defaultView: 'month',
			axisFormat: 'h:mm',
			//height: 'auto',
			eventLimit: true,
			eventSources: [{
				events:json_data,
				ignoreTimezone: false,
				eventDataTransform: function (rawEventData) {
					return {
						id: rawEventData.id,
						title: rawEventData.subject_id,
						start: new Date(rawEventData.start_time),
						end: new Date(rawEventData.end_time),
						description: "<p>id: " + rawEventData.id + 
									"<br><p>code: " + rawEventData.code +
									"<br><p>location: " + rawEventData.location +
									"<br><p>score: " + rawEventData.score +
									"<br><p>webcam: " + rawEventData.eyetracking +
									"<br><p>baseline: " + rawEventData.baseline,
						location: rawEventData.location,
						session: rawEventData.subject_session,
						subsession: rawEventData.subject_subsession,
						currentTimezone: 'America/Chicago',
						origin: 'online'
					};
				}
			},{
				events:gcalList,
				ignoreTimezone: false,
				eventDataTransform: function (rawEventData) {
					return {
						id: rawEventData.title,
						title: rawEventData.title,
						start: new Date(rawEventData.start),
						end: new Date(rawEventData.end),
						location: 'lab',
						origin: 'scheduled'
					};
				}
			}],
    		navLinks: true,
			dayClick: function(date, jsEvent, view, resourceObj) {
				$("[data-toggle='popover']").popover('hide');
				console.log('dayclick')
				console.log('day', date.format()); // date is a moment
				if(view.name != 'month'){
    				return;
				} else {
					$('#calendar').fullCalendar('gotoDate',date);
					$('#calendar').fullCalendar('changeView','agendaDay')
				}
			},
			select: function (start, end, jsEvent) {
				console.log('select')
			},
			eventClick: function(event, jsEvent, view) {
				console.log('eventclick');
			},
			eventRender: function (event, element, view) {
				if (event.location == 'home') {
					element[0].style = 'background-color: #ffb3b3 !important';
					eventColor = "#ffb3b3"
					backgroundColor = "#ead0d0"
					LocationInfo = 'home'
					session = "<b>session: </b>" + event.session +"-"+ event.subsession + "<br/>"
				} else if (event.origin == 'scheduled') {
					element[0].style = 'background-color: #98ffa4 !important';
					eventColor = "#98ffa4"
					backgroundColor = "#d3f3d7"
					LocationInfo = 'google'
					session = ""
				} else {
					element[0].style = 'background-color: #b3dcff !important';
					eventColor = "#b3dcff"
					backgroundColor = "#add8e6"
					LocationInfo = 'lab'
					session = "<b>session: </b>" + event.session +"-"+ event.subsession + "<br/>"
				};
				//popover
				element.popover({
					title: "subject: "+ event.title,
					template: popoverTemplate(eventColor,backgroundColor,LocationInfo),
					content: function () {
						session = '';
						if (event.origin != 'scheduled'){
							session = "<b>session: </b>" + event.session + "-" + event.subsession + "<br/>"
						};
						return	"<div>"+
									"<pre style='background-color: #ffffff !important'>"+
									"<p class='popoverContent' id='eventClick' style=font-family: !important;>"+
										"<b>subject: </b>" + event.title + "<br/>"+
										session +
										"<b>location: </b>" + event.location + "<br/>"+
										"<b>start: </b>" + new Date(event.start).toLocaleTimeString() + " GMT-0500" + "<br/>"+
										"<b>end: </b>" + new Date(event.end).toLocaleTimeString() + " GMT-0500" + "<br/>"+
										"<b>origin: </b>" + event.origin + "<br/>"+
									"</p>"+
									"</pre>"+
								"</div>";
					},
					placement: 'auto',
					html: 'true',
					trigger: 'focus',
					animation: 'true',
					container: 'body'
				})
				element.attr('tabindex', -1); // make the element (div) focusable
			},
			complete: function(){
				console.log($(this))
				$(this).fullCalendar('addEventSource', gcalList);
			}
		})		
		if (window.outerWidth < 800){
			$('#calendar').fullCalendar('option', 'height', 'auto');
		};
		//hide popover on prev next click
		$('.fc-prev-button').click(function () {
			$("[data-toggle='popover']").popover('hide');
		});
		$('.fc-next-button').click(function () {
			$("[data-toggle='popover']").popover('hide');
		});
	} else {
		setTimeout(calendarData, 250);
	}	
};

//control table
var json_data, dotprobe_table;
var tooltipList = {
	"id": "index",
	"subject": "subject id",
	"session": "full session number (i.e. 1, 2, 3)",
	"subsession": "part of session (i.e. 1abc, 2a, 2ab, 2abc)",
	"start time (CST)": "begining of task, in ISO format",
	"end time (CST)": "end of task (or subsession, in ISO format",
	"code": "3-digit code identifying condition (active, placebo, wait)",
	"location": "home or lab",
	"score": "session (if full session [1abc]), or sum of subsession(1ab)",
	"slow": "if over 30% of trials have RT>900msec",
	"uploaded": "data has been uploaded to server",
	"baseline": "initial in-lab score"
};

var $td;
function serverData() {
	$.ajax({
		url: "php/get.php", // this is the path to the above PHP script
		type: 'post',
		success: function (data) {
			json_data = JSON.parse(data);
			//if redirect message
			 if (json_data.redirect !== undefined && json_data.redirect){
        		// data.location contains the string URL to redirect to
				console.log('redirect true')
            	window.location.href = json_data.location;
        	} else {
				if (json_data != JSON.parse(data)){
					console.log('not equal')
					dotprobe_table = $('#database').DataTable({
						lengthMenu: [[20, 50, 100, -1], [20, 50, 100, "All"]],
						lengthChange: false,
						responsive: true,
						order: [[ 0, "desc" ]],
						dom: '<"download"B><"search"f>tp',
						buttons: ['csv', {
							text: 'JSON',
							action: function (e, dt, button, config) {
								var data = dt.buttons.exportData();
								$.fn.dataTable.fileSave(new Blob([JSON.stringify(json_data)]),'dotprobe-js.json')
							}
            			}],
						processing: true,
						data: json_data,
						//serverSide: true,
						columns: [
							{"data": "id"},
							{"data": "subject_id"},
							{"data": "subject_session"},
							{"data": "subject_subsession"},
							{"data": "start_time"},
							{"data": "end_time"},
							{"data": "code"},
							{"data": "location"},
							{"data": "score"},
							{"data": "slow"},
							{"data": "uploaded"},
							{"data": "baseline"}],
						initComplete: function (settings) {
							$('#database thead th').each(function () {
								$td = $(this);
								$td.attr('title', tooltipList[$td.text()]);
							});

							/* Apply the tooltips */
							$('#database thead th[title]').tooltip({
								container: 'body',
								position: {
									my: "center bottom-20",
									at: "center top",
									using: function (position, feedback) {
										$(this).css(position);
										$("<div>").addClass("arrow")
										.addClass(feedback.vertical)
										.addClass(feedback.horizontal)
										.appendTo(this);
									}
								}
							});
						}
					});
					//dotprobe_table.buttons().container().prependTo($('#database_filter'));
					$(".download").css({"float": "left", "margin-bottom":'5px'});
					$(".search").css({"float": "right"});
					//highlight table on hover
					$('#database').on('mouseenter', 'td', function () {
						var rowIdx = dotprobe_table.cell(this).index().row;
						$(dotprobe_table.rows().nodes()).removeClass('highlight');
						$(dotprobe_table.rows(rowIdx).nodes()).addClass('highlight');
					});
				} //else {console.log('equal')};
			}
		}
	})
}
