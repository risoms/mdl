var row=''
var monaco_clicked = false
var editor;
// clean code
function cleanCode(source){
	// remove html elements
	var data = source.replace(/<\/?[^>]+(>|$)/g, "").replace(/&lt;-/g, "<-");
	return data;
}

//copy to clipboard
function copyCode(original){
	//clean code
	var data = cleanCode(original);
	// check if copy is possible
	if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
        var textarea = document.createElement("textarea");
        textarea.textContent = data;
        textarea.style.position = "fixed";  // Prevent scrolling to bottom of page in MS Edge.
        document.body.appendChild(textarea);
        textarea.select();
        try {
            return document.execCommand("copy");  // Security exception may be thrown by some browsers.
        } catch (ex) {
            console.warn("Copy to clipboard failed.", ex);
            return false;
        } finally {
            document.body.removeChild(textarea);
        }
    }
}

//download
function downloadCode(name, original){
	//clean code
	data = cleanCode(original);
	//convert to blob and enable download
    var blob = new Blob([data], {type:'text/x-R'});
    var file = document.createElement("a");
    file.download = name + '.R';
    //file.innerHTML = "Download File";
    file.href = window.URL.createObjectURL(blob);
    file.click();
}

// download and copy code 
function codeButton(){
	// mouse enter and leave
	$('.code-container').on({
		mouseenter: function (){
			$('.btn.code').removeClass("hidden");
		},
		mouseleave: function (){
			$('.btn.code').addClass("hidden");
		}
	});
	//create action on click
	function Timer(element, source){
		if (source == 'copy'){
			var _old = 'Copy';
			var _new = 'Copied!';
		} else if (source == 'download'){
			var _old = 'Download';
			var _new = 'Downloading!';
		};
		// set
			element.html(_new);
			element.addClass('active');
		// update
		setTimeout(function() {
			element.html(_old);
			element.removeClass('active');
		}, 1e3)
	};
	//click
	$('.btn.code').on('click', function() {
		var source = $(this).attr('source');
		//update element
		Timer(element=$(this), source=source);
		// if copying
		if (source == 'copy'){
			//copy code
			var data = $('code').html()
			copyCode(data);
		// else if downloading
		} else if (source == 'download'){
			//download code
			var name = $('code').attr('name');
			var data = $('code').html();
			downloadCode(name, data);
		}
	});
}

//popover
function popover(){
	$('.popover-anchor').popover({
		animation: false,
		container: '.table-container',
		trigger: 'focus',
		placement: 'bottom',
		html: true,
		title: function(){
			var title = $(this).attr('link-id')
			return title
		},
		content: function(){
			var title = $(this).attr('link-id')
			return title
		}
	})
}

//get searchbar
function getinput(){
	//get plot type
	var type = $('.figure').attr('type-id');

	//get trial, calibration unique elements
	if (type=='trial'){
		///add trial <a> element
		var event = ''
		///if event is trial, loop 198 times, else [calibration, validation]
		var trial_loop = Array(198).keys();
		//event id
		var event_id = ['trial'];
	//get calibration unique elements
	} else {
		///add nothing
		var event = ''
		///if event is trial, loop 198 times, else [calibration, validation]
		var block_loop = ['calibration','validation'];
		var event_loop = [1,2,3];
		var day_loop = [0,1];
		//event id
		var event_id = ['day','event','block'];
	};
	//for each event
	for (let id of event_id) {
		//get trial/block/event/day value
		if(id=='trial'){var value = $('.figure').attr('trial-id')}
		else if(id=='block'){var value = $('.figure').attr('trial-id')}
		else if(id=='event'){var value = $('.figure').attr('session-id')}
		else if(id=='day'){var value = $('.figure').attr('day-id')};
		//start
		a=[
			event,
			'<div id='+id+'>',
			'<a>, '+id+'</a>',
			'<div class="input-group mb-3 '+id+'">',
			'<div class="input-group-prepend">',
			'<button class="btn btn-outline-secondary dropdown-toggle" type="button" \
			data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"></button>',
			'<div class="dropdown-menu">'
		];
		b=[]
		if(id=='trial'){
			///loop by number of events
			for (let o of trial_loop) { 
				b.push('<a class="dropdown-item" group="'+id+'" href="#">'+ o +'</a>')
			};
		} else if(id=='block'){
			///loop by number of events
			for (let o of block_loop) { 
				b.push('<a class="dropdown-item" group="'+id+'" href="#">'+ o +'</a>')
			};
		} else if(id=='event'){
			///loop by number of events
			for (let o of event_loop) { 
				b.push('<a class="dropdown-item" group="'+id+'" href="#">'+ o +'</a>')
			};
		} else if(id=='day'){
			///loop by number of events
			for (let o of day_loop) { 
				b.push('<a class="dropdown-item" group="'+id+'" href="#">'+ o +'</a>')
			};
		};
		///end
		c=[
			'</div>',
			'</div>',
			'<input disabled type="text" class="form-control '+id+'" value="'+value+'" content="'+id+'" aria-label="TrialNum">',
			'</div>',
			'</div>'
		];	
		d = a.join('\n') + b.join('\n') + c.join('\n')
		//add to html
		$('.title').append(d)
	};
}

// event listenter
$(document).ready(function() {
	//for trials
	$('.trial>.title').on('click', '.dropdown-menu>a', function(){
		console.log('a');
		var select = $(this).text();
		window.location.href = 'https://mdl.psy.utexas.edu/a/webgazer/i/trial/' + '31_0_' + select + '.html' 
	});

	//for calibration/validation
	$('.calibration>.title,.validation>.title').on('click', '.dropdown-menu>a', function(){
		console.log('c');
		var select = $(this).text();
		var element = $(this).attr('content');
		var group = $(this).attr('group');
		if (group=='event'){
			var event = select; 
			var block = $('.form-control.block').val();
			var day = $('.form-control.day').val();
		} else if (group=='block'){
			var event = $('.form-control.event').val(); 
			var block = select;
			var day = $('.form-control.day').val();
		} else if (group=='day'){
			var event = $('.form-control.event').val(); 
			var block = $('.form-control.block').val();
			var day = select;
		};
		window.location.href = 'https://mdl.psy.utexas.edu/a/webgazer/i/cv/' + 'shellie_' + day + '_' + event + '_' + block + '.html' 
	});
});

// download csv
function getCSV(filename) {
	var path = "./csv/" + filename + ".csv";
	var req = new XMLHttpRequest();
	req.open("GET", path, true);
	req.responseType = "blob";

	req.onload = function (event) {
		var blob = req.response;
		var contentType = req.getResponseHeader("content-type");
		var link = document.createElement('a');
		link.href = window.URL.createObjectURL(blob);
		link.download = filename;
		link.click();
	};
	req.send();
}

// code viewer
function codeComplete(){
	$(document).ready(function(){
		$("#code").on("click", function() {
			console.log('test')
			$('.dataTables_wrapper > .code-container').toggle();
			Prism.plugins.NormalizeWhitespace.setDefaults({
				'remove-trailing': true,
				'remove-indent': true,
				'left-trim': true,
				'right-trim': true,
			});
		});
	})
}

// supplimentary table
function additionalTable(){
	for (let id of ['#table1','#table2']) {
		if($(id).length > 0){
			var table = $(id).DataTable({
				lengthMenu: [[20, 50, 100, -1], [20, 50, 100, "All"]],
				searching: false, 
				paging: false, 
				info: false,
				lengthChange: false,
				responsive: true,
				autoWidth: true,
				columnDefs: [
					{responsivePriority: 1, targets: 0},
					{responsivePriority: 2, targets: 1},
					{responsivePriority: 2, targets: 5}
				]
			}).rows().every(function(rowIdx, tableLoop, rowLoop) {
				var data = this.data();
				if (data[data.length-1] < 0.06){
					data[data.length-1] = '<b>' + data[data.length-1] + '</b>';
					this.data(data);
				} else {
					data[data.length-1] = data[data.length-1];
					this.data(data);
				}
			});
		};
	};
};

// logit table
function getLogitTable(){
	if(source=="summary"){
		//row group
		//https://datatables.net/extensions/rowgroup/
		console.log(source)
		logit_table = $('#table').DataTable({
			searching: false, 
			paging: false, 
			info: false,
			lengthChange: false,
			responsive: true,
			aaSorting: [],
			bSort: false,
			ordering: false,
			autoWidth: true,
			columnDefs: [{targets: 0, visible: false}],
			rowGroup: {
				dataSrc: 0,
				endRender: null,
				startRender: function (rows, group) {
					//for each row within group
					rows.nodes().each(function (r) {
						console.log(group)
						console.log(r)
					}); 
					return $('<tr/>')
						.append('<td class="table-group-content">' + group +' (SD)</td>')
						.attr('data-name', group);
				}
			},
			buttons: [{extend: 'csv', title: 'task'}],
			initComplete: function (settings) {
				//generate code
				//codeComplete()
				//download csv file
				$("#csv").on("click", function() {
					console.log('clicked')
					$('#table').DataTable().button('.buttons-csv').trigger();
				});
			}
		})
	//normal
	} else if(source=="demographic"){
		//row group
		//https://datatables.net/extensions/rowgroup/
		console.log(source)
		logit_table = $('#table').DataTable({
			searching: false, 
			paging: false, 
			info: false,
			lengthChange: false,
			responsive: true,
			aaSorting: [],
			bSort: true,
			ordering: false,
			columnDefs: [{targets: 0, visible: false}, {'width': '50%', 'targets': 1}],
			rowGroup: {
				dataSrc: 0,
				endRender: null,
				startRender: function (rows, group) {
					//if only single row within group
					if ((group=='Hispanic or Latino')||(group=='Handedness (Right)')){
						//for each row within group
						rows.nodes().each(function (r) {
							r.style.display = 'none';
							row = r
						});    
						return $('<tr/>')
							.append('<td class="table-group-content">' + group + ' (%)</td><td class="table-group-value">'+$(row).children()[1].textContent+'</td><td class="table-group-value">'+$(row).children()[2].textContent+'</td>')
							.attr('data-name', group);
							//if only single row within group
					} else if ((group=='Age')){
						//for each row within group
						rows.nodes().each(function (r) {
							r.style.display = 'none';
							row = r
						});    
						return $('<tr/>')
							.append('<td class="table-group-content">' + group + ' (SD)</td><td class="table-group-value">'+$(row).children()[1].textContent+'</td><td class="table-group-value">'+$(row).children()[2].textContent+'</td>')
							.attr('data-name', group);
					//if only single row within group and cesd, rrs
					} else if ((group=='Ruminative Response Scale')||(group=='Center for Epidemiologic Studies Depression Scale')){
						//for each row within group
						rows.nodes().each(function (r) {
							r.style.display = 'none';
							row = r
						});    
						return $('<tr/>')
							.append('<td class="table-group-content">' + group + ' (SD)</td><td class="table-group-value">'+$(row).children()[1].textContent+'</td><td class="table-group-value">'+$(row).children()[2].textContent+'</td>')
							.attr('data-name', group);
					//if eye color
					} else if (group=='Eye Color'){
							//for each row within group
							rows.nodes().each(function (r) {
								test = r
								r.style.display = 'none';
								//append class
								class_ = r.className;
								r.className = class_ + " group-item";
								//set new attribute
								r.setAttribute("type", group)
							}); 
							return $('<tr/>')
								.append('<td group="'+group+'" class="table-group-content large-group">' + group +' (%)</td>')
								.attr('data-name', group);
					//if cesd
					} else if (group=='Center for Epidemiologic Studies Depression Scale'){
						//for each row within group
						rows.nodes().each(function (r) {
							console.log(group); 
							console.log(r);
						});    
						return $('<tr/>')
							.append('<td colspan="2" class="table-group-content">' + group + '</td>')
							.attr('data-name', group);
					//if normal
					} else {
						//for each row within group
						rows.nodes().each(function (r) {
						}); 
						return $('<tr/>')
							.append('<td class="table-group-content">' + group +' (%)</td>')
							.attr('data-name', group);
					}
				}
			},
			buttons: [{extend: 'csv', title: 'demographic'}],
			initComplete: function (settings) {
				//hide/show columns
				$(".large-group").on("click", function() {
					//get group of button clicked
					group = $(this).attr('group');
					//hide all other groups
					//$('.group-item').hide();
					//show relevant group
					$("[type='"+group+"']").toggle();
					console.log('enter task');
					console.log(group);
				});
				//download csv file
				$("#csv").on("click", function() {
					console.log('clicked')
					$('#table').DataTable().button('.buttons-csv').trigger();
				});
			}
		})
	} else if(source=="full_summary"){
		//row group
		//https://datatables.net/extensions/rowgroup/
		console.log(source)
		logit_table = $('#table').DataTable({
			searching: true, 
			paging: false, 
			info: false,
			lengthChange: false,
			responsive: true,
			autoWidth: true,
			//https://datatables.net/extensions/responsive/classes
			columns: [
				{data: "participant", className:"all"},
				{data: "session", className:"all"}
			],
			buttons: [{extend: 'csv', title: source}],
			initComplete: function (settings) {
				//hide/show columns
				$(".large-group").on("click", function() {
					//get group of button clicked
					group = $(this).attr('group');
					//hide all other groups
					//$('.group-item').hide();
					//show relevant group
					$("[type='"+group+"']").toggle();
					console.log('enter task');
					console.log(group);
				});
				//download csv file
				$("#csv").on("click", function() {
					console.log('clicked')
					$('#table').DataTable().button('.buttons-csv').trigger();
				});
			}
		})
	} else if(source=="definitions"){
		//row group
		//https://datatables.net/extensions/rowgroup/
		console.log(source)
		logit_table = $('#table').DataTable({
			searching: true, 
			paging: false, 
			info: false,
			lengthChange: false,
			responsive: true,
			autoWidth: true,
			//https://datatables.net/extensions/responsive/classes
			columns: [
				{data: "variable", className:"all"},
				{data: "group", className:"all"},
				{data: "type", className:"all"},
				{data: "example", className:"none"},
				{data: "definition", className:"none"},
			],
			columnDefs: [
				{responsivePriority: 1, targets: 0},
				{responsivePriority: 1, targets: 1},
				{responsivePriority: 1, targets: 2}
			],
			buttons: [{extend: 'csv', title: 'definitions'}],
			initComplete: function (settings) {}
		})
	//device
	} else if(source=="device"){
		//row group
		//https://datatables.net/extensions/rowgroup/
		console.log(source)
		logit_table = $('#table').DataTable({
			searching: false, 
			paging: false, 
			info: false,
			lengthChange: false,
			responsive: true,
			aaSorting: [],
			bSort: false,
			ordering: false,
			columnDefs: [{targets: 0, visible: false}, {'width': '60%', 'targets': 1}],
			rowGroup: {
				dataSrc: 0,
				endRender: null,
				startRender: function (rows, group) {
					if (group=='Luminance'){
						//for each row within group
						rows.nodes().each(function (r) {
							r.style.display = 'none';
							row = r
						});    
						return $('<tr/>')
							.append('<td class="table-group-content">' + group + ' (SD)</td><td class="table-group-value">'+$(row).children()[1].textContent+'</td>')
							.attr('data-name', group);
					//if gpu model, Browser version, Operating System version, Webcam brand, Display resolution
					} else if ((group=='GPU model') || (group=='Browser version') || (group=='Operating System version') || (group=='Webcam brand') || (group=='devicePixelRatio') ||
					(group=='Display resolution') || (group=='Operating System') || (group=='Browser') || (group=='GPU type') || (group=='Webcam resolution') || (group=='Webcam message') ){
						//for each row within group
						rows.nodes().each(function (r) {
							test = r
							r.style.display = 'none';
							//append class
							class_ = r.className;
							r.className = class_ + " group-item";
							//set new attribute
							r.setAttribute("type", group)
						}); 
						return $('<tr/>')
							.append('<td group="'+group+'" class="table-group-content large-group">' + group +' (%)</td>')
							.attr('data-name', group);
					//if normal
					} else {
						//for each row within group
						rows.nodes().each(function (r) {
						}); 
						return $('<tr/>')
							.append('<td class="table-group-content">' + group +' (%)</td>')
							.attr('data-name', group);
					}
				}
			},
			buttons: [{extend: 'csv', title: 'device'}],
			initComplete: function (settings) {
				//hide/show columns
				$(".large-group").on("click", function() {
					//get group of button clicked
					group = $(this).attr('group');
					//hide all other groups
					//$('.group-item').hide();
					//show relevant group
					$("[type='"+group+"']").toggle();
					console.log('enter device');
					console.log(group);
				});
				//generate code
				//codeComplete()
				//download csv file
				$("#csv").on("click", function() {
					console.log('clicked')
					$('#table').DataTable().button('.buttons-csv').trigger();
				});
			}
		})
	//task
	} else if(source=="task"){
		//row group
		//https://datatables.net/extensions/rowgroup/
		console.log(source)
		logit_table = $('#table').DataTable({
			searching: false, 
			paging: false, 
			info: false,
			lengthChange: false,
			responsive: true,
			aaSorting: [],
			bSort: false,
			ordering: false,
			columnDefs: [{targets: 0, visible: false}, {width: '45%', targets: 1}],
			rowGroup: {
				dataSrc: 0,
				endRender: null,
				startRender: function (rows, group) {
					if (group=='Task'){
						group_pct = ''
						//for each row within group
						rows.nodes().each(function (r) {
							//r.style.display = 'none';
							row = r
							row_content = r.children[0].textContent
							if (row_content=="Task"){
								//get pct from task and add to group
								group_pct = r.children[1].textContent
								//hide row
								r.style.display = 'none';
							}
						});    
						return $('<tr/>')
							.append('<td class="table-group-content">' + group + 
							' (%)<a class="note" href="#1"><sup>1</sup></a></td><td class="table-group-value">'+group_pct+'</td>')
							.attr('data-name', group);
					//add anchor
					} else if(group=='Eyetracking') {
						//for each row within group
						rows.nodes().each(function (r) {
							console.log(group)
							console.log(r)
						}); 
						return $('<tr/>')
							.append('<td class="table-group-content">' + group +' (%) </td>')
							.attr('data-name', group);
					} else {
						//for each row within group
						rows.nodes().each(function (r) {
							console.log(group)
							console.log(r)
						}); 
						return $('<tr/>')
							.append('<td class="table-group-content">' + group +' (%)</td>')
							.attr('data-name', group);
					}
				}
			},
			buttons: [{extend: 'csv', title: 'task'}],
			initComplete: function (settings) {
				//generate code
				//codeComplete()
				//download csv file
				$("#csv").on("click", function() {
					console.log('clicked')
					$('#table').DataTable().button('.buttons-csv').trigger();
				});
				//set subgroup font-size smaller
				var subgroup = ["Calibrated","Used"]
				for (let o of ["Calibrated","Used"]) {
					// $('td:contains("'+o+'")').parent().css({'cssText':'font-size:12px !important','color':'#444'});
					$('td:contains("'+o+'")').parent().css({'color':'#444'});
					$('td:contains("'+o+'")').css({'cssText':'padding-left:40px !important'});
					//$('td:contains("'+o+'")').parent().children().css({'padding':'3px'});
				};
			}
		})
	//normal
	} else if(source=="logit"){
		console.log(source)
		logit_table = $('#table').DataTable({
			lengthMenu: [[20, 50, 100, -1], [20, 50, 100, "All"]],
			searching: false, 
			paging: false, 
			info: false,
			lengthChange: false,
			responsive: true,
			autoWidth: true,
			//https://datatables.net/extensions/responsive/classes
			columns: [
				{data: "term", className:"all"},
				{data: "B", className:"desktop"},
				{data: "SE", className:"desktop"},
				{data: "z", className:"desktop"},
				{data: "Pr(>|z|)", className:"all"},
				{data: "OR", className:"all"},
				{data: "95% CI", className:"all"},
			],
			// columnDefs: [
			// 	{responsivePriority: 1, targets: 0},
			// 	{responsivePriority: 2, targets: 1},
			// 	{responsivePriority: 2, targets: 3}
			// ],
			buttons: [{extend: 'csv', title: 'logit'}],
			initComplete: function (settings) {
				//generate code
				codeComplete()
				//get data source from #table
				filename = $('#table').attr("data-file")
				//download csv file
				$("#csv").on("click", function() {
					console.log('download')
					getCSV(filename)
				});
			}
		}).rows().every(function(rowIdx, tableLoop, rowLoop) {
			var data = this.data();
			if(source=="logit"){
				if ((data[data.length-3] < 0.06) && (data[data.length-3] > 0.01)){
					data[data.length-3] = '<b>' + data[data.length-3] + '</b>';
					this.data(data);
				} else if (data[data.length-3] < 0.0001) {
					data[data.length-3] = '<b>< 0.0001</b>';
					this.data(data);
				} else {
					data[data.length-3] = data[data.length-3];
					this.data(data);
				}
			}
		})
	} else if(source=="anova"){
		console.log(source)
		logit_table = $('#table').DataTable({
			lengthMenu: [[20, 50, 100, -1], [20, 50, 100, "All"]],
			searching: false, 
			paging: false, 
			info: false,
			lengthChange: false,
			responsive: true,
			autoWidth: true,
			columns: [
				{data: "index", responsivePriority:1},
				{data: "term", responsivePriority:1},
				{data: "SS", responsivePriority:2},
				{data: "MS", responsivePriority:2},
				{data: "N", responsivePriority:3},
				{data: "DF", responsivePriority:3},
				{data: "f", responsivePriority:1},
				{data: "Pr(>|f|)", responsivePriority:1},
			],
			buttons: [{extend: 'csv', title: 'onset'}],
			initComplete: function (settings) {
				//generate code
				codeComplete()
				//get data source from #table
				filename = $('#table').attr("data-file")
				//download csv file
				$("#csv").on("click", function() {
					console.log('download')
					getCSV(filename)
				});
			}
		}).rows().every(function(rowIdx, tableLoop, rowLoop) {
			var data = this.data();
			if(source=="anova"){
				if ((data['Pr(>|f|)'] < 0.06) && (data['Pr(>|f|)'] > 0.01)){
					data['Pr(>|f|)'] = '<b>' + data['Pr(>|f|)'] + '</b>';
					this.data(data);
				} else if (data['Pr(>|f|)'] < 0.0001) {
					data['Pr(>|t|)'] = '<b>< 0.0001</b>';
					this.data(data);
				} else {
					data['Pr(>|f|)'] = data['Pr(>|f|)'];
					this.data(data);
				}
			}
		})
	} else if(source=="onset"){
		console.log(source)
		logit_table = $('#table').DataTable({
			lengthMenu: [[20, 50, 100, -1], [20, 50, 100, "All"]],
			searching: false, 
			paging: false, 
			info: false,
			lengthChange: false,
			responsive: true,
			autoWidth: true,
			columns: [
				{data: "index", responsivePriority:1},
				{data: "term", responsivePriority:1},
				{data: "B", responsivePriority:2},
				{data: "SE", responsivePriority:3},
				{data: "DF", responsivePriority:3},
				{data: "t", responsivePriority:1},
				{data: "Pr(>|t|)", responsivePriority:1},
			],
			buttons: [{extend: 'csv', title: 'onset'}],
			initComplete: function (settings) {
				//generate code
				codeComplete()
				//get data source from #table
				filename = $('#table').attr("data-file")
				//download csv file
				$("#csv").on("click", function() {
					console.log('download')
					getCSV(filename)
				});
			}
		}).rows().every(function(rowIdx, tableLoop, rowLoop) {
			var data = this.data();
			if(source=="onset"){
				if ((data['Pr(>|t|)'] < 0.06) && (data['Pr(>|t|)'] > 0.01)){
					data['Pr(>|t|)'] = '<b>' + data['Pr(>|t|)'] + '</b>';
					this.data(data);
				} else if (data['Pr(>|t|)'] < 0.0001) {
					data['Pr(>|t|)'] = '<b>< 0.0001</b>';
					this.data(data);
				} else {
					data['Pr(>|t|)'] = data['Pr(>|t|)'];
					this.data(data);
				}
			}
		})
	} else {
		console.log(source)
		logit_table = $('#table').DataTable({
			lengthMenu: [[20, 50, 100, -1], [20, 50, 100, "All"]],
			searching: false, 
			paging: false, 
			info: false,
			lengthChange: false,
			responsive: true,
			autoWidth: true,
			initComplete: function (settings) {}
		})
	}
	//hover
	if((source!="full_summary") && (source!="demographic") && (source!="device") && (source!="logit") && (source!="onset") && (source!="anova") && (source!="definitions") && (source!="task") && (source!="summary")){	
		//highlight table on hover
		$('#table').on('mouseenter', 'td', function () {
			var rowIdx = logit_table.cell(this).index().row;
			$(logit_table.rows().nodes()).removeClass('highlight');
			$(logit_table.rows(rowIdx).nodes()).addClass('highlight');
		});
	};
}
