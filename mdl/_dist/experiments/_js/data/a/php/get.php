<?php
/* by: Semeon Risom (8/23/17)
 * email: semeon.risom@gmail.com
 * description: get data from database for dashboard
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

//check if in range for these ip addresses
$lowip = ip2long('129.116.89.65');
$highip = ip2long('129.116.89.126');
$adminip = ip2long('129.116.89.104');
$j_shumakeip = ip2long('146.6.51.176');
$j_shumakeip2 = ip2long('128.83.185.41');

//if ip address > low range or ip address < high range or matching urls
if ((ip2long($userip) <= $highip && $lowip <= ip2long($userip)) ||
	(ip2long($userip) === $j_shumakeip) ||
	(ip2long($userip) === $j_shumakeip2) || 
	(ip2long($userip) === $adminip)){
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
	$query = mysqli_query($link, "SELECT
								`id`,
								`subject_id`,
								`subject_session`,
								`subject_subsession`,
								`start_time`,
								`end_time`,
								`location`,
								`code`,
								`score`,
								`slow`,
								`uploaded`,
								`baseline`
								FROM `$table` ORDER BY `id`");

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
} else {
	echo json_encode(array("redirect"=>true,"location"=>"fail.html"));
	exit;
};
?>