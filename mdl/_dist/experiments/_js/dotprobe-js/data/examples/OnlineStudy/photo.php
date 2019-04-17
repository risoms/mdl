<?php
    session_start();

    $subject = htmlspecialchars($_SESSION['subjectno']);
    include("study.php");

    if ($subject != "" && is_dir('data/'.$_STUDY.'/'.$subject)) {
        $rawData = $_POST['imgBase64'];
        $filteredData = explode(',', $rawData);
        $unencoded = base64_decode($filteredData[1]);

        $datime = date("YmdHis", time()); # - 3600*7

        // name & save the image file
        $fp = fopen('data/' . $_STUDY . '/' . $subject . '/' . $_STUDY . '_' . $subject . '_photo_' . $datime . '.jpg', 'w');
        fwrite($fp, $unencoded);
        fclose($fp);
    }
?>