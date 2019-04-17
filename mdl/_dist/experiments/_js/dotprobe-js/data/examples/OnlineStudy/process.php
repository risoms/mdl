<?php
    session_start();

    $d = $_POST['data'];
    if(!$_SESSION['subjectno']) {
        $s = file_get_contents("data/subjectno.txt");
        file_put_contents("data/subjectno.txt", ($s+1), LOCK_EX);
        $_SESSION['subjectno'] = $s;
    } else {
        $s = $_SESSION['subjectno'];
    }
    include("study.php");
    $e = $_STUDY;

    // experimental path
    $p = 'data/' . $e;
    if (!is_dir($p)) {
        mkdir($p);
        chmod($p, 0777);
    }

    // path of subject
    $p = $p . "/" . $s;
    if (!is_dir($p)) {
        mkdir($p);
        chmod($p, 0777);
    }

    // final complete path prefix, e.g. data/tolcampilot/1/tolcam_1_
    $p = $p . "/".$e. "_".$s."_";


    // txt file, e.g. data/tolcampilot/1/tolcam_1_2_calibration_5.txt
    if ($d['type'] == "info") {
        $fn = $p . "" . $d['type'] . ".txt";
    } else if ($d['type'] == "validationfail") {
        $fn = $p . "" . ($d['block']+1) . "_" . $d['type'] . "_" . ($d['trial']+1) . "_". $d['attempt'].".txt";
    } else {
        $fn = $p . "" . ($d['block']+1) . "_" . $d['type'] . "_" . ($d['trial']+1) . ".txt";
    }
    $fh = fopen($fn, "w");
    switch($d['type']) {
        case "calibration":
            fwrite($fh, "subject\tblock\tcalibration_no\tdatapoint\ttime\tx\ty\tcx\tcy\tdistance\tcalibration_count\r\n");
            for ($j = 0; $j < count($d["raw"]); $j++) {
                fwrite($fh,
                    sprintf("%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\r\n",
                    $s, ($d["block"]+1), ($d["trial"]+1), ($j+1), $d["raw"][$j]["time"], $d["raw"][$j]["x"], $d["raw"][$j]["y"], $d["raw"][$j]["cx"], $d["raw"][$j]["cy"], $d["raw"][$j]["dist"], $d["raw"][$j]["c"])
                );
            }
            break;

        case "validation":
        case "validationfail":
            fwrite($fh, "subject\tblock\tvalidation_no\tdatapoint\ttime\tx\ty\tvx\tvy\tdistance\tvalidation_count\tvalid\r\n");
            for ($j = 0; $j < count($d["raw"]); $j++) {
                // data.validations[validation_no].raw.push({'time': clock, 'x': d.x, 'y': d.y, 'vx': validation_current.x, 'vy': validation_current.y, 'dist': dist, 'c': c, 'valid': 0});
                fwrite($fh,
                    sprintf("%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\r\n",
                        $s, ($d["block"]+1), ($d["trial"]+1), ($j+1), $d["raw"][$j]["time"], $d["raw"][$j]["x"], $d["raw"][$j]["y"], $d["raw"][$j]["vx"], $d["raw"][$j]["vy"], $d["raw"][$j]["dist"], $d["raw"][$j]["c"], $d["raw"][$j]["valid"])
                );
            }
            break;

        case "trial":
            fwrite($fh, "subject\tblock\ttask\ttrial_no\tdatapoint\ttime\tcondition\tx\ty\ttx\tty\tstatus\r\n");
            for ($j = 0; $j < count($d["raw"]); $j++) {
                fwrite($fh, sprintf("%s\t%d\t%s\t%d\t%d\t%d\t%s\t%d\t%d\t%d\t%d\t%s\r\n", $s, ($d["block"]+1), $d["task"], ($d["trial"]+1), ($j+1), $d["raw"][$j]["time"], $d["condition"], $d["raw"][$j]["x"], $d["raw"][$j]["y"], $d["raw"][$j]["tx"], $d["raw"][$j]["ty"], $d["raw"][$j]["status"]));
            }

            break;

        case "info":
            fwrite($fh, "subject\tscreen_width\tscreen_height\tua\tconsent\tbirthday\tgender\tvisual\tident\r\n");
            fwrite($fh, sprintf("%s\t%d\t%d\t%s\t%s\t%s\t%s\t%s\t%s\r\n", $s, $d["screen_width"], $d["screen_height"], $d["ua"], $d["consent"], $d["birthday"], $d["gender"], $d["visual"], $d["ident"]));
            break;
    }
    fclose($fh);

?>


