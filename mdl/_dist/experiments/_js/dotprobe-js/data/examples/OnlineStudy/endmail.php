<?php
session_start();
$s = $_SESSION['subjectno'];

$blacklist = array(
    '127.0.0.1',
    '::1'
);

if ($s != "" && !in_array($_SERVER['REMOTE_ADDR'], $blacklist)) {
    $nachricht = "<html><body>New data at ". (isset($_SERVER['HTTPS']) ? "https" : "http") . "://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]" . "<br />\n";
    $nachricht .= "</body></html>";

    $header  = 'MIME-Version: 1.0' . "\r\n";
    $header .= 'Content-type: text/html; charset=iso-8859-1' . "\r\n";
    $header .= 'From: Entwicklungsneuropsychologie RUB <kilian.semmelmann@rub.de>'. "\r\n" .
        'Reply-To: Kilian Semmelmann <kilian.semmelmann@rub.de>'. "\r\n" .
        'X-Mailer: PHP/' . phpversion();

    mail('kilian.semmelmann@gmail.com', '[TOLcam | '. $s .'] finished', $nachricht, $header);

    echo "mail sent";
}