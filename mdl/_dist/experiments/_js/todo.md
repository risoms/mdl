# dotprobe
# Attention Bias Modification for Major Depressive Disorder: Effects on Attention Bias, Resting State Connectivity, and Symptom Change
## stim ---------done
* remove border
* resize images to 768x768
* for images smaller, add black border
* center svg canvas

## trials---------done
* create excel sheet for parameters
* embed trial sheet into js
* be able to run trials in task


## trial structure---------done
+ make sure practice trials are implimented as expected (stim_time, probe_time)
+ remove fixation after stim onset
+ display probe
+ timing
+ POFA = 3,000 ms
* fixation for 1,500 ms, followed by an image pair. 
+ IAPS pairs for 4,500ms
* practice max accuracy

## ---------------done
* have system setup to be able to keep track of version participant needs to run online (note subject should be running same version each day: i.e. control, control, control)
* grey background for stim (task should match requirements of eyetracking setup)
* face detection (jspsych-xyz) should take 2-3minutes before forcing behavioral version of task
* check if neutral and sad stim alternate sides of screen
	scenes: no pairs, random placement (left/right)
	faces: pairs, random placement (left/right)

## ---------------done 6/5
* eyetracking: fix terminate issue
* make sure: POFA: 12 trials, IAPS: 10 trials
* create iaps trials

## ---------------done 6/7
* before emailing Kean
** enable number pad responses of 8 and 9 as well
** for first session, recieve both condition and participant name as two uri's
	*** https://utw10625.utweb.utexas.edu/app/dotprobe-js/?uname=tt&cndt=b	
## ---------------done 6/19
* instead of 24 delay between sessions, use day (i.e. session 1: Nov 30 5:00pm, earliest session 2: Nov 31 200am)
* pause the task if fullscreen has been exited with a simple method to revert it back
* if eyetracking version doesnt work the first time at home, force behavioral version at home for each subsequent session
	** variable: webcamStatus - 
		NotAllowedError (blocked by browser), 
		PreviousFail (browser not working last session)
		Success - allowed to stream
* add breaks after third block ("you now have a brief break; please press the spacebar when ready to proceed again")
* Macc/MRT: calculate and use as score
	** in email: ask if score should be calulated as score = (num_correct_resp/198) /(mean_rt) [i.e. 100/7500]
	** both rt and num_correct_resp collected
* include variable for congruent/incongruent trials in csv
	** ie: trial was congruent (stimulus and probe are in the same visual field, i.e., the probe appeared where the sad stimulus was), or incongruent (stimulus and probe are in opposite visual fields)
* debug jspsychxyz and calibration
	** include feedback to the user so that they know if they're on the right track with moving/position their head.
	**  make this calibration process much faster at determining whether or not it can track someone's face or just abandon the web-cam element
	** resolve keans macbook webcam issue (see email)
	** create button that allows recalculation of camera-coordinates.js (headtracker)
	** if time attempting xyz is greater than 3 minutes, create button to skip calibration and force behavioral

## ---------------done 6/27
* have the ABM program utilize a unique randomly assigned 3-character alphanumeric code (Sent by jason) to identify which treatment group the individual is in

## ---------------done 7/19
* E-mail updates to the research coordinator
* cut the length of the at-home training to be 1/4 of the in-lab time if possible
* for the webcam calibration to have a note about when the participant should stay still versus try to move to adjust the camera
* small tweak to the feedback page and include a simple smiley face if they are below the RTCO and a frowny face if they are above the RTCO
## ---------------done 8/17
* allow multiple sessions per day (remove 24 hour window)
* check to make sure active condition and placebo conditions trials are working correctly
* XXXXXXXXXXXXXXXX (not needed if time to 1/4)Having the table data from the training session push to the database list at each break. 
* XXXXXXXXXXXXXXXX (not needed if time to 1/4) and Having the csv data from the training session push to the server at each break.
* XXXXXXXXXXXXXXXX provide graph for task after session, showing scores for previous 5 sessions 
# to do
## now------------------------------------------------------------------------------------------------ 
* fix unusual issue with recording participant xy coordinate in eyetracker. xy not updating (see placebo_3abc.csv)
* create variable that calculate if participants are not "3 SD above their mean RT at baseline, in-lab testing" in their most recent training session
	** http://blog.cemsimsek.com/post/121207530538/standard-deviation-in-javascript
	** https://stackoverflow.com/questions/7343890/standard-deviation-javascript
	** baseline will be sent to task as URI: "rtco"
## second (send update after finished)------------------------------------------------------------------- 
### revert settings
#### done
* add to each php page
	/*prevent direct access*/
	if(!isset($_SERVER['HTTP_REFERER'])){
		// redirect them to your desired location
		header( 'HTTP/1.0 403 Forbidden', TRUE, 403 );
		exit;
	}
	/*check if in range for campus ip*/
	$userip = $_SERVER["HTTP_X_FORWARDED_FOR"]; //get ipaddress
	$lowip = ip2long('129.116.89.65');
	$highip = ip2long('129.116.89.126');
	//print("lowip: ".$lowip."\r\nhighip: ".$highip."\r\nipstr: ".ip2long($userip));
	if (ip2long($userip) <= $highip && $lowip <= ip2long($userip)) {
		//print("in range\r\n");
		$currlocation = "lab";
	} else {
		//print("out of range\r\n");
		$currlocation = "home";
	};
	//print($currlocation."\r\n");
* /data/a/php/get.php
	**//if (($highip <= ip2long($userip)) || (ip2long($userip) <= $lowip)) { ------ return after debug
* email.php
	** $mail->addBCC('comparemindtrial@utexas.edu');
** data/a/js/user.js
	path: window.location.origin + '/a/dotprobe-js/src/csv/data/subject', 
	ajaxAction: window.location.origin + '/a/dotprobe-js/data/a/php/FileExplorer/',
* https://redcap.prc.utexas.edu/redcap/redcap_v7.5.2/ProjectSetup/index.php?pid=1397
		Enable optional modules and customizations:  Data Entry Trigger
		url of website https://mdl.psy.utexas.edu/a/r33/data/redcap/index.php
* general
	** change email address to comparemindtrial@utexas.edu
#### to do
* database
	** add dotprobe_table and lookup_table to mdl.psych database
	** turn off allow user to download
	** turn off debug mode
* remove semeon.risom@gmail.com from
	** data/redcap/index.php
	** src/php/email.php
	
### consider including in dashboard
	** options
		*** calendar
		*** download
		*** table
		*** graph
		*** Upcoming participants (today)
		*** Recent participants (this week)
		*** Inactive participants (less than...)
		*** Participants to send Reminder email to (have email to click function)
		*** calendar
		*** study info
			*** json list of variables (from participant csv)
		*** expandable list of participants: https://dribbble.com/shots/2084101-Dashboard-Overview/attachments/374756
	** (from kean) allow study coordinator to see
		*** who's currently enrolled in training, 
		*** how many sessions they've completed over the past week, 
		*** how many sessions they've completed total, 
		*** percentage of sessions they should have completed at this point in their training, 
		*** how many hours ago their last training session was (with some sort of flagging if it's been more than 24 hours), 
		*** %accuracy and RT for that last session (again flagged if concerning performance)


## (later) wheel of faces analysis @@@@@@@@@@@@@@@@@@@@@@

