<?php
/* by: Semeon Risom (8/23/17)
 * email: semeon.risom@gmail.com
 * description: get data from database before begining experiment
 * php version: 5.6.25
*/
/*prevent direct access by url*/
if(!isset($_SERVER['HTTP_REFERER'])){
    // redirect them to your desired location
    header( 'HTTP/1.0 403 Forbidden', TRUE, 403 );
    exit;
};

/*query request*/;
$subject = "'".$_POST[subject]."'";
$code = "'".$_POST[code]."'";
//echo $subject."\r\n";

/*SQL server connection information*/
$host = 'mysql.utweb.utexas.edu';
$user = 'utw10623';
$pass = '98J8q89tqwIl3wHq';
$db = 'r33';

/*get user location - home or lab*/
//get ipaddress
$userip = $_SERVER["HTTP_X_FORWARDED_FOR"];
$userhost = gethostbyaddr($userip); //print("ip: ".$userip."\r\nhostname: ".$userhost."\r\n");

//check if in range for campus ip
$lowip = ip2long('129.116.89.65');
$adminip = ip2long('129.116.89.104');
$highip = ip2long('129.116.89.126');
if (ip2long($userip) <= $highip && $lowip <= ip2long($userip)) {
	$currlocation = "lab"; //print("in range\r\n");
} else {
	$currlocation = "home"; //print("out of range\r\n");
};

//check if admin ip
if (ip2long($userip) == $adminip){
	$isAdmin = true;
} else {
	$isAdmin = false;
};

/*Connect to mysql database*/
$link = mysqli_connect($host, $user, $pass, $db);

/*get group matching participant code (condition) i.e. code: A00, group: placebo*/
$get_group = mysqli_query($link, "SELECT `group` FROM `lookup_table` WHERE `code` = $code");
$cndt = mysqli_fetch_assoc($get_group);

//check if condition is not matching code
if ($cndt['group'] === NULL){
	$cndt['group'] = 'missing';
};

/*get participant data*/
$table = 'dotprobe_table';
$query = mysqli_query($link, "SELECT * FROM `$table` WHERE `subject_id` = $subject ORDER BY `subject_session` DESC LIMIT 1");

/*Create the data output array for JSON*/
$output = array();
while($rows = mysqli_fetch_assoc($query)){
    $output[] = $rows;
};

/*compare previous and current dates to see if 24hrs have passed*/
/*todays date*/
date_default_timezone_set("America/Chicago"); 
$date1 = date("Y-m-d H:i:s");
$day1 = date('Y-m-d', strtotime($date1)); //extract current day

/*original session*/
$date0 = $output[0]['start_time'];
$day0 = date('Y-m-d', strtotime($date0)); //extract original day

//if new subject: number of rows = 0
if (mysqli_num_rows($query)==0){
	//send to task
	$output[0]['ready'] = "new";
	$output[0]['location'] = $currlocation;
	$output[0]['isAdmin'] = $isAdmin;
	$output[0]['condition'] = $cndt['group'];
	echo json_encode($output);
//previous subject
} else {
	//send to task
	$output[0]['ready'] = "go";
	$output[0]['location'] = $currlocation;
	$output[0]['isAdmin'] = $isAdmin;
	$output[0]['condition'] = $cndt['group'];
	echo json_encode($output);
};		

/*Frees the memory from result*/
mysqli_free_result($get_group);
mysqli_free_result($query);

/*Closes database connection*/
mysqli_close($link);
?>