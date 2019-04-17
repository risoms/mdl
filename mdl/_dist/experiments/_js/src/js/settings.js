/**
 * Settings configuration
 */
var iterate = 0;
//note: onset/offset times are within their respective events (not trial level)
var settings = {
	//calibration level
	expName:'dotprobe_js',
	trials: 21,
	blocks: undefined,
	stimulus_onset: 1500,
	pofa_offset: 3000,
	iaps_offset: 4500,
	cue_offset: 10000,
	canvas_size: [window.innerWidth,window.innerHeight],
	img_directory: 'src/img/stim/',
	element_directory: 'src/img/',
	fixation_image: 'src/img/fixation.png',
	cue_image: 'cue.jpg',
	mask_image: 'mask.jpg',
	fixation_size: [32,32],
	cue_size: [112,112],
	stimulus_size: [600,600],
	canvas_width: 1366,
	canvas_height: 768,
 }

//prevents progress div from being used when not needed
var loop=1;
var ua = detect.parse(navigator.userAgent);
var browser = ua.browser.family;

//calculate screen and inner values after multiplying for devicepixelratio
display_monitor = [(window.screen.width*window.devicePixelRatio)+"x"+(window.screen.height*window.devicePixelRatio)];
display_window = [(window.innerWidth*window.devicePixelRatio)+"x"+(window.innerHeight*window.devicePixelRatio)];
var subject = {
	os: ua.os.name,
	browser: ua.browser.name,
	display_monitor: display_monitor,
	display_window: display_window,
	webcam_size: -1,
	webcam_used: null,
	lum:-1,
	devicePixelRatio: window.devicePixelRatio
 };

var calibration_coordinates = [
	['25%', '75%'], ['50%', '75%'], ['75%', '75%'], ['25%', '50%'], ['50%', '50%'], ['75%', '50%'], ['25%', '25%'], ['50%', '25%'], ['75%', '25%']
];

function get_date(){
	d = new Date();
	curr_day = ("0"+d.getUTCDate()).slice(-2);
	curr_month = ("0"+ (d.getUTCMonth() + 1)).slice(-2);
	curr_year = d.getUTCFullYear();
	curr_time = ("0"+d.getUTCHours()).slice(-2)+""+("0"+d.getUTCMinutes()).slice(-2)
	full_date = curr_year +"_" + curr_month + "_" + curr_day + "_" + curr_time;
	return full_date
};
settings.date = get_date();

//display dimensions'
function diagonal_dimensions(){
	inch = document.write("<div id='ppi' style='height: 1in; width: 1in; left: 100%; position: fixed; top: 100%;'></div>")
	//ratio of the (vertical) size of one physical pixel to device independent pixels(dips)
	//usually devicePixelRatio=1, excluding high dpi devices (iphone)
	devicePixelRatio = window.devicePixelRatio || 1;
	//pixel density per inch (x,y)
	ppi_x = document.getElementById('ppi').offsetWidth * devicePixelRatio,
	ppi_y = document.getElementById('ppi').offsetHeight * devicePixelRatio;
	//screen size (inch)
	width_in = screen.width / ppi_x,
	height_in = screen.height / ppi_y,
	diagonal_inches = (Math.sqrt(width_in * width_in + height_in * height_in)).toFixed(2);
	return diagonal_inches;
}
var diagonal_inches = diagonal_dimensions();

