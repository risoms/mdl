<?php
/* by: Semeon Risom (8/23/17)
 * email: semeon.risom@gmail.com
 * description: send email if score is above threshold
 * php version: 5.6.25
*/
/*prevent direct access by url*/
if(!isset($_SERVER['HTTP_REFERER'])){
    // redirect them to your desired location
    header( 'HTTP/1.0 403 Forbidden', TRUE, 403 );
    exit;
};

/*pre-reqs*/
require_once('reqs/class.phpmailer.php');

//get reason for email
$purpose = $_POST[purpose];

/*Create a new PHPMailer instance*/
$mail = new PHPMailer();
$mail->isHTML(true);  // Set email format to HTML

//address
/*sender*/ $mail->setFrom('root@utweb-wb-z1-p01.its.utexas.edu', 'MDL-R33');
/*reply-to*/ $mail->addReplyTo('comparemindtrial@utexas.edu', 'R33 Coordinator');
/*recipient*/ $mail->addAddress('comparemindtrial@utexas.edu', 'R33 Coordinator');

//if purpose is to notify of issue running the task
if($purpose == 'rtco') {
	/*query request*/
	$subject = "'".$_POST[subject]."'";
	$session = "'".$_POST[session]."'";
	$date = "'".$_POST[end_time]."'";
	$score = "'".$_POST[score]."'";
	$baseline = "'".$_POST[baseline]."'";
	
	/*message*/
	$m = '<html><body>';
	$m .= 'subject: '.$subject.'<br>';
	$m .= 'session-subsession: '.$session.'<br>';
	$m .= 'date (CST): '.$date.'<br>';
	$m .= 'score (dotprobe-js): '.$score.'<br>';
	$m .= 'baseline (REDCap): '.$baseline.'<br>';
	$m .= '</body></html>';
	
	/*subject*/ $mail->Subject = "[R33][dotprobe-js] Participant $subject's score > baseline";
	
//if purpose is to notify coordinator of fail score
} else if ($purpose == 'fail') {
	/*query request*/
	$reason = $_POST[reason];
	$url = $_POST[url];
	
	//get location
	$userip = $_SERVER["HTTP_X_FORWARDED_FOR"];
	
	//get range
	$lowip = ip2long('129.116.89.65');
	$adminip = ip2long('129.116.89.104');
	$highip = ip2long('129.116.89.126');
	
	//get current location variable
	if (ip2long($userip) <= $highip && $lowip <= ip2long($userip)) {
		$currlocation = "lab";
	} else {
		$currlocation = "home";
	};
	
	/*query request*/
	date_default_timezone_set('America/Chicago');
	$date = date('Y-m-d h:i:s');
	
	/*message*/
	$m = '<html><body>';
	$m .= 'date (CST): '.$date.'<br>';
	$m .= 'location: '.$currlocation.'<br>';
	$m .= 'reason: '.$reason.'<br>';
	$m .= 'url: '.$url.'<br>';
	$m .= '</body></html>';
	
	/*subject*/ $mail->Subject = '[R33][dotprobe-js] experiment failure';
};

/*body*/ $mail->Body = $m;

/*send the message, check for errors*/
if(!$mail->Send()) {
	echo json_encode("Mailer Error: " . $mail->ErrorInfo);
} else {
	echo json_encode($m);
};
?>