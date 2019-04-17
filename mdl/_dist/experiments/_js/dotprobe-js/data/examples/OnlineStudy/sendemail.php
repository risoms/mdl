<?php
session_start();
$s = $_SESSION['subjectno'];
$m = nl2br(htmlspecialchars($_POST['content']));

$blacklist = array(
    '127.0.0.1',
    '::1'
);

if ($s != "" && !in_array($_SERVER['REMOTE_ADDR'], $blacklist)) {
    $nachricht = "<html><body>\n" . $m;
    $nachricht .= "</body></html>";

    $header  = 'MIME-Version: 1.0' . "\r\n";
    $header .= 'Content-type: text/html; charset=iso-8859-1' . "\r\n";
    $header .= 'From: Entwicklungsneuropsychologie RUB <kilian.semmelmann@rub.de>'. "\r\n" .
        'Reply-To: Kilian Semmelmann <kilian.semmelmann@rub.de>'. "\r\n" .
        'X-Mailer: PHP/' . phpversion();

    mail('kilian.semmelmann@gmail.com', '[TOLcam | '. $s .'] sends a message', $nachricht, $header);

    echo "mail sent";
}