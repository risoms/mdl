<?php
/* by: Semeon Risom (8/23/17)
 * email: semeon.risom@gmail.com
 * description: upload participant data to server
 * php version: 5.6.25
*/
/*prevent direct access by url*/
if(!isset($_SERVER['HTTP_REFERER'])){
	// redirect them to your desired location
	header( 'HTTP/1.0 403 Forbidden', TRUE, 403 );
	exit;
};

/*get user location*/
$userip = $_SERVER["HTTP_X_FORWARDED_FOR"];
//admin ipaddress
$adminip = ip2long('129.116.89.104');

/*get subject name, data, and directory*/
$filename = $_POST['fname'];
$data = $_POST['fdata'];
$subsession = $_POST['subsession'];
if (ip2long($userip) == $adminip) {
	if ($subsession == 'abc') {
		$dir = "../csv/data/admin/";
	} else {
		$dir = "../csv/data/admin/part/";
	}
} else {
	if ($subsession == 'abc') {
		$dir = "../csv/data/subject/";
	} else {
		$dir = "../csv/data/subject/part/";
	}
};

/*check if filename exists*/
if (file_exists($dir.$filename)) {
	echo "The file $filename exists";
	$rand = mt_rand(100, 999);
	$fp = fopen($dir.$filename."_".$rand, 'w');
	fwrite($fp, $data);
	fclose($fp);
} else {
	echo "The file $filename does not exist.";
	$fp = fopen($dir.$filename, 'w');
	fwrite($fp, $data);
	fclose($fp);
}
?>