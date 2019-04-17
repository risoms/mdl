<?php
/* by: Semeon Risom (8/23/17)
 * email: semeon.risom@gmail.com
 * description: send email after recieving redcap data for assessment
 * php version: 5.6.25
*/
/*data entry trigger: https://redcap.prc.utexas.edu/redcap/redcap_v7.5.2/ProjectSetup/index.php?pid=1397*/
/*pre-reqs*/
require_once('reqs/class.phpmailer.php');

/*recap advanced link*/
//send and recieve redcap api tokens
$GLOBALS['api_token'] = 'D19832E1ACE0B3A502F2E41E05057C20';
$GLOBALS['api_url'] = 'https://redcap.prc.utexas.edu/redcap/api/';
$GLOBALS['project_url'] = 'https://redcap.prc.utexas.edu/redcap/redcap_v7.5.2/index.php?pid=1397';

/*POST request*/
$project_id = "'".$_POST[project_id]."'";
$record = "'".$_POST[record]."'"; //record id
$instrument = "'".$_POST[instrument]."'"; //ie eligibility_screen
$eligibility_complete = "'".$_POST[eligibility_screen_complete]."'";
$origin = $_POST[project_url];
$email_text = var_export($_POST, true);

/*php log - in case of error*/
//ob_start();
//phpinfo();
//$info = ob_get_contents();
//ob_end_clean();
//$fp = fopen("phpinfo.php", "w+");
//fwrite($fp, $info);
//fclose($fp);

/*get date of POST request*/
date_default_timezone_set('America/Chicago');
$date = date('d-m-Y h:i:s a');

/*email*/
//if missing post request (likely from attempting access through source other than redcap)
if(empty($origin)){
	$origin = "";
};

//if redcap event is eligibility_screen and eligibility_screen is complete [0=Incomplete, 1=Unverified, 2=Complete]
if(($instrument == "'eligibility_screen'") && ($eligibility_complete=="'2'")) {
	//get data from redcap
	$data = array(
		'token' => $GLOBALS['api_token'],
		'content' => 'record',
		'format' => 'json',
		'type' => 'flat',
		'records' => $record,
		'fields' => array('es_eligible','es_email'),
		'forms' => array('eligibility_screen'),
		'events' => array('online_eligibility_arm_1'),
		'rawOrLabel' => 'raw',
		'rawOrLabelHeaders' => 'raw',
		'exportCheckboxLabel' => 'false',
		'exportSurveyFields' => 'false',
		'exportDataAccessGroups' => 'false',
		'returnFormat' => 'json'
	);
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $GLOBALS['api_url']);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_VERBOSE, 0);
	curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
	curl_setopt($ch, CURLOPT_AUTOREFERER, true);
	curl_setopt($ch, CURLOPT_MAXREDIRS, 10);
	curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
	curl_setopt($ch, CURLOPT_FRESH_CONNECT, 1);
	curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data, '', '&'));
	$output = curl_exec($ch);
	print $output;
	curl_close($ch);

	//extract variables data from redcap
	$decoded = json_decode($output,true); //convert to object
	$email = $decoded[0]['es_email']; //email address
	$esQualify = intval($decoded[0]['es_qualify']); //if es_qualify = 28, then send email
	$QIDSScore = intval($decoded[0]['es_qidssr_total']); //did subject qualify [1=true, 0=false]
	$participate = intval($decoded[0]['no_participate']); //does subject want to participate [1=true, 0=false]
	$es_availability_time = $decoded[0]['es_availability_time']; //times available for phone screen 
	$es_meds = intval($decoded[0]['es_meds']); //using medication
	$immediate_screen = intval($decoded[0]['immediate_screen']); //available for immediate screening
	//if using meds
	if ($es_meds === 1) {
		$es_medchange = intval($decoded[0]['es_medchange']); //medication change
	} else {
		$es_medchange = 999;
	};

	//if eligibility success and subject wants to participate send email
	if(($esQualify === 27) && ($participate === 1)){
		//get date
		date_default_timezone_set('America/Chicago'); 
		$d0 = new DateTime();
		//email
		$m = '<html><body>';
		//if available for immediate screening
		if ($immediate_screen === 1) {
			$m .= "<strong>Available for immediate screening</strong><br>";
			$m .= "<br>";
		};
		$m .= "REDCap Record ID: $record<br>";
		$m .= "date (day-month-year): $date<br>";
		$m .= "email: $email<br>";
		$m .= "REDCap instrument: $instrument<br>";
		$m .= "REDCap project url: $origin<br>";
		$m .= "REDCap project id: $project_id<br>";
		$m .= "Qualify Score: '$esQualify'<br>";
		$m .= "QIDS-SR Baseline Total Score: '$QIDSScore'<br>";
		$m .= "Availability Times: '$es_availability_time'<br>";
		//Not currently using medication
		if ($es_meds === 0) {
			$m .= "Not currently using medication for emotional problems.<br>";
		//D) 12 or more weeks ago
		} elseif ($es_medchange === 3) {
			$m .= "Change in Medication: 12 or more weeks ago<br>";
		//C) 8 to 11 weeks ago
		} elseif ($es_medchange === 2) {
			$d0->modify('+4 week'); //reschedule date
			$d1 = $d0->format('Y-m-d');
			$m .= "Change in Medication: 8 to 11 weeks ago ('+4 weeks')<br>";
			$m .= "Earliest participation date: '$d1' (y-m-d)<br>";
		//B) 4 to 8 weeks ago
		} elseif ($es_medchange === 1) {
			$d0->modify('+8 week'); //reschedule date
			$d1 = $d0->format('Y-m-d');
			$m .= "Change in Medication: 4 to 8 weeks ago ('+8 weeks')<br>";
			$m .= "Earliest participation date: '$d1' (y-m-d)<br>";
		//A) Less than 4 weeks ago
		} elseif ($es_medchange === 0) {
			$d0->modify('+12 week'); //reschedule date
			$d1 = $d0->format('Y-m-d');
			$m .= "Change in Medication: Less than 4 weeks ago ('+12 weeks')<br>";
			$m .= "Earliest participation date: '$d1' (y-m-d)<br>";
		};
		//$m .= "post data: $email_text<br>";
		//$m .= "<br>";
		//$m .= "api data: $output<br>";
		$m .= "</body></html>";

		/*Create a new PHPMailer instance*/
		$mail = new PHPMailer();
		$mail->isHTML(true);  // Set email format to HTML

		//flag as important
		//if available for immediate screening
		if ($immediate_screen === 1) {
			$mail->AddCustomHeader("X-MSMail-Priority: High"); //microsoft outlook
			$mail->addCustomHeader("X-Priority: 1");
			$mail->addCustomHeader("Importance: High");
		};

		//address
		/*sender*/ $mail->setFrom('root@utweb-wb-z1-p01.its.utexas.edu', 'MDL-R33');
		/*reply-to*/ $mail->addReplyTo('comparemindtrial@utexas.edu', 'R33 Coordinator');
		/*recipient*/ $mail->addAddress('comparemindtrial@utexas.edu', 'R33 Coordinator');
		/*recipient*/ //$mail->addAddress('semeon.risom@gmail.com', 'Semeon');

		//message
		//if available for immediate screening
		if ($immediate_screen === 1) {
			/*subject*/ $mail->Subject = "[R33][assessment][medication][availability][immediate] Record ID: $record";
		} else {
			/*subject*/ $mail->Subject = "[R33][assessment][medication][availability] Record ID: $record";
		};
		/*body*/ $mail->Body = $m;

		/*send the message, check for errors*/
		if(!$mail->Send()) {
			echo json_encode("Mailer Error: " . $mail->ErrorInfo);
		} else {
			echo json_encode($m);
		};
	};
};
?>