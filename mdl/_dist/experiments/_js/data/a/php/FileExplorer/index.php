<?php
header('Access-Control-Allow-Origin: *');
header("Content-Type: application/json");

require_once("FileExplorerOperations.php");

if($_REQUEST["json"]!= null || $_REQUEST["Path"]){
    if($_REQUEST["json"]!= null)
        $args = json_decode($_REQUEST["json"], true);
    else
        $args = $_REQUEST;

    $result= "";
    $feObj = new FileExplorerOperations();

    switch($args["ActionType"]){
        case "Read": 
            $result = $feObj ->Read($args["Path"], $args["ExtensionsAllow"]);
            break;
        case "CreateFolder":
            $result = $feObj ->CreateFolder($args["Path"], $args["Name"]);
            break;
        case "Remove":
            $result = $feObj ->Remove($args["Names"], $args["Path"]);
            break;
        case "Rename":
            $result = $feObj ->Rename($args["Path"], $args["Name"], $args["NewName"], $args["CommonFiles"] );
            break;
        case "GetDetails":
            $result = $feObj ->GetDetails($args["Path"], $args["Names"] );
            break;
        case "Upload":
            $result = $feObj ->Upload($_FILES["FileUpload"], $args["Path"] );
            break;
        case "Paste":
            $result = $feObj ->Paste($args["LocationFrom"], $args["LocationTo"], $args["Names"], $args["Action"], $args["CommonFiles"]);
            break;
        case "Search":
            $result = $feObj ->Search($args["Path"], $args["ExtensionsAllow"], $args["SearchString"], $args["CaseSensitive"]);
            break;
        case "Download":
            $fileNames = array();
            $selectedItems = json_decode($_REQUEST['SelectedItems'], true);
            for($i=0 ; $i< count($selectedItems); $i++){
                array_push($fileNames, $selectedItems[$i]["name"]);                
            }
            $result = $feObj ->Download($args["Path"], $fileNames);
            break;
        case "GetImage":
			$result = $feObj ->GetImage($args["Path"], $args["CanCompress"], json_decode($args["Size"]));
            break;
    }
	if($_GET['callback']){
		$result = json_encode($result);
		$functionName = $_GET['callback'];
		echo "$functionName($result);";
	}		
	else{
		echo json_encode($result);
	}
    
}


?>