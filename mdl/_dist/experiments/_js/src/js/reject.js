//block safari users and make request for running task in chrome, edge, internet explore, firefox
//safari seems to not allow requestfullscreen to work correctly
function checkBrowser(){
	console.log('%c0.checking browser...','color: orange');
	ua = detect.parse(navigator.userAgent);
	browser = ua.browser.family;
	url = window.location.href;
	//Chrome version 15+, Firefox 10+ and Safari 5.1+ 
	if (browser=='safari'||browser=='Safari'||browser=='Mobile Safari'||browser==''||
		browser=='Edge'||browser=='MSIE'||browser=='IEMobile'){
		console.log('%c0.browser incompatiable...','color: orange');
		remove_container = $('.container')
		remove_container.remove()
		document.write('<style>.imgContainer{float:left; width: calc(100%/3);}</style>');
		$(document.body).append(
			'<script src="dist/js/jquery-3.1.0.min.js"></script>'
			+'<link href="dist/css/jspsych.css" rel="stylesheet" type="text/css">'
			+'<link href="dist/css/experiment.css" rel="stylesheet" type="text/css">'
			+'<div class="container">'
				+'<div class="container-inner">'
					+'<p>Your browser will not be able to run this experiment.</p>'
					+'<p>Instead, please access the experiment (link below) on one of the following browsers.</p>'
					+'<div class="image123">'
						+'<div class="imgContainer">'
							+'<a href="https://www.google.com/chrome/browser/desktop/">'
								+'<img src="dist/img/chrome.png" height="150" width="150"/>'
							+'</a>'
							+'<p>Chrome (preferred) </p>'
						+'</div>'
						+'<div class="imgContainer">'
							+'<a href="https://www.mozilla.org/en-US/firefox/new/">'
								+'<img src="dist/img/firefox.png" height="150" width="150"/>'
							+'</a>'
							+'<p>Firefox</p>'
						+'</div>'
						+'<div class="imgContainer">'
							+'<a href="http://www.opera.com/download">'
								+'<img src="dist/img/opera.png" height="150" width="150"/>'
							+'</a>'
							+'<p>Opera</p>'
						+'</div>'
						+'<a href="'+url+'">'
							+'<p>'+url+'</p>'
						+'</a>'
					+'</div>'
				+'</div>'
			+'</div>'
		);
		$.holdReady(true);
		throw new Error("browser incompatiable");
	}
};

function wait_until(start_date, wait_date){
	//get url
	url = window.location.href;
	document.write(
		'<style>.imgContainer{'
		+'float:left;'
		+'width: 25%;'
		+'}</style>'
	)
	document.write(
		'<script src="dist/js/jquery-3.1.0.min.js"></script>'
		+'<link href="dist/css/jspsych.css" rel="stylesheet" type="text/css">'
		+'<link href="dist/css/experiment.css" rel="stylesheet" type="text/css">'
		+'<div class="container">'
			+'<div class="container-inner">'
				+'<p>The task can not begin. You have participated on '+start_date+' CST.</p>'
				+'<p>The task will be available on '+wait_date+' CST.</p>'
				+'<div class="image123">'
					+'<a href="'+url+'">'
						+'<p>'+url+'</p>'
					+'</a>'
				+'</div>'
			+'</div>'
		+'</div>'
	);
	$.holdReady(true);
}

function sessionfail(){
	//get url
	url = window.location.href;
	document.write(
		'<style>.imgContainer{'
		+'float:left;'
		+'width: 25%;'
		+'}</style>'
	)
	document.write(
		'<script src="dist/js/jquery-3.1.0.min.js"></script>'
		+'<link href="dist/css/jspsych.css" rel="stylesheet" type="text/css">'
		+'<link href="dist/css/experiment.css" rel="stylesheet" type="text/css">'
		+'<div class="container">'
			+'<div class="container-inner">'
				+'<p>The task can not begin. Please alert the researchers.</p>'
				+'<div class="image123">'
					+'<a href="'+url+'">'
						+'<p>'+url+'</p>'
					+'</a>'
				+'</div>'
			+'</div>'
		+'</div>'
	);
	$.holdReady(true);
}