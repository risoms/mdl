<?php
/*
 * php version: 5.6.25
 */
/*prevent direct access by url*/
if(!isset($_SERVER['HTTP_REFERER'])){
    // redirect them to your desired location
    header( 'HTTP/1.0 403 Forbidden', TRUE, 403 );
    exit;
};

/*prevent access from non IMHR computers*/
//get ipaddress
$userip = $_SERVER["HTTP_X_FORWARDED_FOR"];
//print("ip: ".$userip."\r\n");

//check if in range for campus ip
$lowip = ip2long('129.116.89.65');
$highip = ip2long('129.116.89.126');
//print("lowip: ".$lowip."\r\nhighip: ".$highip."\r\nipstr: ".ip2long($userip));

//if ip address < low range or ip address > high range
//if (($highip <= ip2long($userip)) || (ip2long($userip) <= $lowip)) { ------ return after debug
if ((empty($userip))) {
	echo json_encode(array("redirect"=>true,"location"=>"fail.html"));
    exit;
	
} else {
	/*query request*/;
	$subject = "'".$_POST[subject]."'";
	//echo $subject."\r\n";

	/*SQL server connection information*/
	$host = 'mysql.utweb.utexas.edu';
	$user = 'utw10623';
	$pass = '98J8q89tqwIl3wHq';
	$db = 'r33';
	$table = 'dotprobe_table';

	/*Connect to mysql database*/
	$link = mysqli_connect($host, $user, $pass, $db);

	/*Execute an SQL query on the database*/
	$query = mysqli_query($link, "SELECT `id`,`subject_id`,`subject_session`,`subject_subsession`,`start_time`,`end_time`,`location`,`code`,`score`,`slow`,`baseline` FROM `$table` ORDER BY `id`");

	/*Create the data output array for JSON*/
	$output = array();
	while($rows = mysqli_fetch_assoc($query)){
		$output[] = $rows;
	};

	/*sending JSON ready output array*/
	echo json_encode($output);

	/*Frees the memory from result*/
	mysqli_free_result($query);

	/*Closes database connection*/
	mysqli_close($link);
};
?>