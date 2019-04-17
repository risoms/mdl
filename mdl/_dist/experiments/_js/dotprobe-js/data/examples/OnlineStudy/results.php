<?php
session_start();
if (isset($_GET['save'])) {
    $ead = nl2br(htmlspecialchars($_POST['email']));
    $f = fopen('data/results.txt', 'a');
    fprintf($f, "%s\r\n", $ead);
    fclose($f);
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>the online lab</title>
    <meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
    <script type="text/javascript" src="js/jquery-1.12.3.min.js"></script>
    <link rel="stylesheet" type="text/css" href="css/jquery.mobile.structure-1.4.2.min.css" />
    <link rel="stylesheet" type="text/css" href="css/results.css" />
</head>
<body>
<div id="header">

</div>
<h1>Ergebnisse der Studie</h1>
<div id="content">
    Thank you very much for your participation and your interest in our study.
    <?php
    if (isset($_GET['save'])) {
        echo "We will send you the results of this study as soon as they are published.";
    } else {
        ?>
        To get information about the results of the study, please enter your email address above. This address will be saved completely separate from any other data to keep anonymity.
        <br/><br/>
        <form action="?save" method="POST">
            <input type="text" style="width: 500px;" name="email"/><input type="submit" value="save" />
        </form>
        <?php
    }
    ?>
</div>

</body>
</html>
