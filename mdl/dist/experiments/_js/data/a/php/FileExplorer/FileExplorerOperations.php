<?php
error_reporting(E_ERROR | E_PARSE);


Abstract class BasicFileOperations
{
	abstract public function Read($path, $filter, $selectedItems = null);
	abstract public function CreateFolder($path, $name, $selectedItems = null);
	abstract public function Remove($names, $path, $selectedItems = null);
	abstract public function Rename($path, $oldName, $newName, $commonFiles, $selectedItems = null);
	abstract public function GetDetails($path, $names, $selectedItems = null);
	abstract public function Paste($sourceDir, $targetDir, $names, $option, $commonFiles, $selectedItems = null, $targetFolder = null);
	abstract public function Upload($files, $path, $selectedItems = null);
	abstract public function Download($path, $names, $selectedItems = null);
	abstract public function GetImage($path, $canCompress = false, $size= null, $selectedItems = null);
	abstract public function Search($path, $filter, $searchString, $caseSensitive, $selectedItems = null);
	
	public function IsSharedServer($path){
		if(preg_match('#^//.+#i', $path) && !preg_match('#^//.+/.+#i', $path))
			return true;
		else
			return false;
	}
	public function IsSharedPath($path){
		if(preg_match('#^//.+#i', $path) && !strpos($path, "//" . $_SERVER[HTTP_HOST]) !== false)
			return true;
		else
			return false;
	}
	public function IsPhysicalPath($path){
		if((strpos($path, ':') !== false) && (!strpos($path, "//" . $_SERVER[HTTP_HOST]) !== false))
			return true;
		else
			return false;
	}
	public function IsNullOrEmptyString($string){
		return (!isset($string) || trim($string)==='');
	}
	public function GetPhysicalPath($absolutePath){
		if ($this->IsSharedPath($absolutePath))
		return $absolutePath;
		return $this->IsPhysicalPath($absolutePath) ? $absolutePath : ($_SERVER["DOCUMENT_ROOT"] . DIRECTORY_SEPARATOR . $absolutePath);
	}
	public function ToAbsolute($virtualPath){
		if ($this->IsSharedPath($virtualPath) || $this->IsPhysicalPath($virtualPath))
			return $virtualPath;
		if ($this->IsNullOrEmptyString($virtualPath)){
			return null;
		}
		return parse_url($virtualPath, PHP_URL_PATH);
	}
	public function FindRatio($originalSize, $targetSize){
		$aspectRatio =  $originalSize->Width / $originalSize->Height;
		$width = $targetSize->Width;
		$height = $targetSize->Height;
		if($originalSize->Width > $targetSize->Width || $originalSize->Height > $targetSize->Height){
			if($aspectRatio > 1){
				$height = $targetSize->Height / $aspectRatio;
			}
			else{
				$width = $targetSize->Width * $aspectRatio;
			}
		}
		else{
			$width = $originalSize->Width;
			$height = $originalSize->Height;        
		}
		$imageSize = new ImageSize();
		$imageSize->Width = max($width, 1);
		$imageSize->Height = max($height, 1); 
		return $imageSize;
	}
	public function CompressImage($path, $targetSize){
		$fullPath = $this->GetPhysicalPath($this->ToAbsolute($path));
		$info = getimagesize($fullPath);
		if ($info['mime'] == 'image/jpeg')
			$imageOriginal = imagecreatefromjpeg($fullPath);
		elseif ($info['mime'] == 'image/gif')
			$imageOriginal = imagecreatefromgif($fullPath);
		elseif ($info['mime'] == 'image/png')
			$imageOriginal = imagecreatefrompng($fullPath);
		else 
			$imageOriginal = false;
		$originalSize->Width= $info[0];
		$originalSize->Height = $info[1];
		$targetSize = $this->FindRatio($originalSize, $targetSize);
		$imageResized = imagecreatetruecolor($targetSize->Width, $targetSize->Height);
		$white = imagecolorallocate($imageResized, 255, 255, 255);
		imagefill($imageResized, 0, 0, $white);
		imagecopyresampled($imageResized, $imageOriginal, 0, 0, 0, 0, $targetSize->Width, $targetSize->Height, $originalSize->Width, $originalSize->Height);		
		imagepng($imageResized);
	}
	public function CanReplace($path, $commonFiles){
		if($commonFiles != null){
			foreach ($commonFiles as $file){
				if ($file[Path] == $path)
					return $file[IsReplace];
			}
		}
		return true;
	}
	public function RemoveDirectory($path) {
		$files = glob($path . '/*');
		foreach ($files as $file) {
			is_dir($file) ? $this->RemoveDirectory($file) : unlink($file);
		}
		rmdir($path);
		return;
	}
}
/**
 * FileExplorerOperations short summary.
 *
 * FileExplorerOperations description.
 *
 * @version 1.0
 * @author syncfusion
 */
class FileExplorerOperations extends BasicFileOperations
{
	public $ExtensionsAllow ="*";
	

	#region BasicFileOperations Members

	/**
	 *
	 * @param  $path 
	 * @param  $filter 
	 * @param  $selectedItems 
	 */
	function Read($path, $filter, $selectedItems = null){
		try{
			$this->ExtensionsAllow = $filter;
			$response = new FileExplorerResponse();
			$directoryContent = array();
			if($this->IsSharedPath($path)){
				if(!is_dir($path))
					throw new Exception($path. ' - directory is not available');
			}
			else{
				$path = $this->GetPhysicalPath($this->ToAbsolute($path));
			}
			$files= array_diff(scandir($path), array('..', '.'));
			foreach ($files as $filename) {
				$fullName= $path . $filename;
				$preventAdd = false;
				$isFile = is_file($fullName);
				if($isFile && ($filter != null && $filter != "*" && $filter != "*.*") && !(strpos($filter, pathinfo($fullName, PATHINFO_EXTENSION)) !== false)){
					$preventAdd = true;
				}
				if(!$preventAdd){
					$filedetails = new FileExplorerDirectoryContent();
					$filedetails->name = $filename;
					$filedetails->type = $isFile ? "File" : "Directory";
					$filedetails->isFile = $isFile;
					$filedetails->hasChild = $isFile ? false : count(glob($fullName. "/*", GLOB_ONLYDIR))  > 0 ;
					$filedetails->size= $isFile ? filesize($fullName) : "";
					$filedetails->dateModified = date("F d Y H:i:s.", filemtime($fullName));
					array_push($directoryContent, $filedetails);
				}
			}
			$response->files = $directoryContent;
			return $response;
		}
		catch(Exception $e) {
			$response->error = $e->getMessage();
			return $response;
		}
	}
	
	/**
	 *
	 * @param  $path 
	 * @param  $name 
	 * @param  $selectedItems 
	 */
	function CreateFolder($path, $name, $selectedItems = null)
	{      
		try{
			$response = new FileExplorerResponse();
			$path = $this->GetPhysicalPath($this->ToAbsolute($path));
			$folderPath = $path. DIRECTORY_SEPARATOR . $name;
			if (!is_dir($folderPath)) {
				mkdir($folderPath, 0777, true);
			}
			$response->files= array(0 => array("name"=>$name));
			return $response;
		}
		catch(Exception $e) {
			$response->error = $e->getMessage();
			return $response;
		}		
	}

	/**
	 *
	 * @param  $names 
	 * @param  $path 
	 * @param  $selectedItems 
	 */
	function Remove($names, $path, $selectedItems = null)
	{
		try{			
			$fileCount= count($names);
			$path = $this->GetPhysicalPath($this->ToAbsolute($path));
			for($i=0; $i < $fileCount; $i++){
				$fullPath = $path. DIRECTORY_SEPARATOR . $names[$i];
				if (file_exists($fullPath)) {
					if(is_file($fullPath))
						unlink($fullPath);
					else
						$this->RemoveDirectory($fullPath);						
				}
			}
			return "";
		}
		catch(Exception $e) {
			$response = new FileExplorerResponse();
			$response->error = $e->getMessage();
			return $response;
		}
	}

	/**
	 *
	 * @param  $path 
	 * @param  $oldName 
	 * @param  $newName 
	 * @param  $commonFiles 
	 * @param  $selectedItems 
	 */
	function Rename($path, $oldName, $newName, $commonFiles, $selectedItems = null)
	{
		try {
			$path = $this->GetPhysicalPath($this->ToAbsolute($path));
			rename($path. DIRECTORY_SEPARATOR . $oldName, $path. DIRECTORY_SEPARATOR . $newName);
			return "";
		}
		catch(Exception $e) {
			$response = new FileExplorerResponse();
			$response->error = $e->getMessage();
			return $response;
		}
	}

	/**
	 *
	 * @param  $path 
	 * @param  $names 
	 * @param  $selectedItems 
	 */
	function GetDetails($path, $names, $selectedItems = null)
	{
		try {
			$response = new FileExplorerResponse();
			$directoryContent = array();
			$path = $this->GetPhysicalPath($this->ToAbsolute($path));
			foreach ($names as $filename) {
				$fullName= $path . $filename;
				$isFile = is_file($fullName);
				$filedetails = new FileDetails();
				$filedetails->Name = $filename;
				$filedetails->Type = $isFile ?  pathinfo($fullName, PATHINFO_EXTENSION) : "Directory";
				$filedetails->Location = $fullName;
				$filedetails->Size = $isFile ? filesize($fullName) : "";
				$filedetails->Created = date("F d Y H:i:s.", filectime($fullName));
				$filedetails->Modified = date("F d Y H:i:s.", filemtime($fullName));
				array_push($directoryContent, $filedetails);
			}
			$response->details = $directoryContent;
			return $response;
		}
		catch(Exception $e) {			
			$response->error = $e->getMessage();
			return $response;
		}
	}

	/**
	 *
	 * @param  $sourceDir 
	 * @param  $targetDir 
	 * @param  $names 
	 * @param  $option 
	 * @param  $commonFiles 
	 * @param  $selectedItems 
	 * @param  $targetFolder 
	 */
	function Paste($sourceDir, $targetDir, $names, $option, $commonFiles, $selectedItems = null, $targetFolder = null)
	{
		try {
			if ($commonFiles != null)
			{
				foreach ($commonFiles as $index => $file)
				{
					$commonFiles[$index][Path] = $this->GetPhysicalPath($this->ToAbsolute($file[Path]));
				}
			}			
			$response = new FileExplorerResponse();
			$directoryContent = array();
			$sourceDir = $this->GetPhysicalPath($this->ToAbsolute($sourceDir));
			$targetDir = $this->GetPhysicalPath($this->ToAbsolute($targetDir));
			if($option == "move"){
				foreach($names as $fileName){
					if( strcmp($sourceDir, $targetDir) != 0 && $this->CanReplace($targetDir . $fileName, $commonFiles)){
						$result=  rename($sourceDir . $fileName, $targetDir . $fileName);
					}
				}
			}else{
				foreach($names as $fileName){
					$temp = $fileName;
					if(is_file($sourceDir . $fileName)){						
						if(strcmp($sourceDir, $targetDir) == 0){
							for($i=1; file_exists( $targetDir . $temp); $i++){
								$temp = pathinfo($fileName)["filename"] . "(" . $i . ")." . pathinfo($fileName)["extension"];
							}
							$result=  copy($sourceDir . $fileName, $targetDir . $temp);
						}
						elseif($this->CanReplace($targetDir . $fileName, $commonFiles)){
							$result=  copy($sourceDir . $fileName, $targetDir . $temp);
						}
					}
					else{
						if(strcmp($sourceDir, $targetDir) == 0){
							for($i=1; file_exists($targetDir . $temp); $i++){
								$temp = $fileName . "(" . $i . ")";
							}							
							$this->CopyFolder($sourceDir . $fileName, $targetDir . $temp);
						}
						elseif($this->CanReplace($targetDir . $fileName, $commonFiles)){
							$this->CopyFolder($sourceDir . $fileName, $targetDir . $temp);
						}
					}
						
				}
			}
			$response->files = $directoryContent;
			return $response;
		}
		catch(Exception $e) {
			$response->error = $e->getMessage();
			return $response;
		}
	}
	function CopyFolder($source, $target) {        
		$dir = opendir($source);
		@mkdir($target); 
		while(false !== ( $file = readdir($dir)) ) { 
			if (( $file != '.' ) && ( $file != '..' )) { 
				if ( is_dir($source . '/' . $file) ) { 
					$this->CopyFolder($source . '/' . $file,$target . '/' . $file); 
				} 
				else { 
					copy($source . '/' . $file, $target . '/' . $file); 
				} 
			} 
		} 
		closedir($dir); 
	} 

	/**
	 *
	 * @param  $files 
	 * @param  $path 
	 * @param  $selectedItems 
	 */
	function Upload($files, $path, $selectedItems = null)
	{
		try{
			$response = new FileExplorerResponse();
			$path = $this->GetPhysicalPath($this->ToAbsolute($path));
			$target_file = $path . basename($files["name"]);
			if (move_uploaded_file($files["tmp_name"], $target_file)) {
				return "The file ". basename( $files["name"]). " has been uploaded successfully.";
			}
			else{
				throw new Exception("Error in upload");
			}
		}
		catch(Exception $e) {
			$response->error = $e->getMessage();
			return $response;
		}
	}

	/**
	 *
	 * @param  $path 
	 * @param  $names 
	 * @param  $selectedItems 
	 */
	function Download($path, $names, $selectedItems = null)
	{
		try {
			if($names != null && count($names) > 1){
				$fullPath = $this->GetPhysicalPath($this->ToAbsolute($path));
				$zip_folder = new ZipArchive();
				$temp_file = tempnam('.','');
				$zip_folder->open($temp_file, ZipArchive::CREATE);
				foreach($names as $file){
					$file = $fullPath . $file;
					$download_file = file_get_contents($file);
					$zip_folder->addFromString(basename($file),$download_file);
				}
				$zip_folder->close();
				header('Content-disposition: attachment; filename=Files.zip');
				header('Content-type: application/zip');
				readfile($temp_file);
				if (file_exists($temp_file) && is_file($temp_file)){
					unlink($temp_file);
				}
			}
			else{
				$fullPath = $this->GetPhysicalPath($this->ToAbsolute($path));
				if(count($names) == 1){
					$fullPath = $fullPath . $names[0];
				}
				header('Content-Description: File Transfer');
				header('Content-Type: application/force-download');
				header("Content-Disposition: attachment; filename=\"" . basename($fullPath) . "\";");
				header('Content-Transfer-Encoding: binary');
				header('Expires: 0');
				header('Cache-Control: must-revalidate');
				header('Pragma: public');
				header('Content-Length: ' . filesize($fullPath));
				ob_clean();
				flush();
				readfile($fullPath);
				exit;
			}
		}
		catch(Exception $e) {
			$response = new FileExplorerResponse();
			$response->error = $e->getMessage();
			return $response;
		}
	}

	/**
	 *
	 * @param  $path 
	 * @param  $canCompress 
	 * @param  $size 
	 * @param  $selectedItems 
	 */
	function GetImage($path, $canCompress = false, $size = null, $selectedItems = null)
	{
		try {
			if($canCompress != "false" && $canCompress){
				$this->CompressImage($path , $size);
			}
			else{
				$fullPath = $this->GetPhysicalPath($this->ToAbsolute($path));
				header('Content-Description: File Transfer');
				header('Content-Type: application/force-download');
				header("Content-Disposition: attachment; filename=\"" . basename($fullPath) . "\";");
				header('Content-Transfer-Encoding: binary');
				header('Expires: 0');
				header('Cache-Control: must-revalidate');
				header('Pragma: public');
				header('Content-Length: ' . filesize($fullPath));
				ob_clean();
				flush();
				readfile($fullPath);
				exit;
			}
		}
		catch(Exception $e) {
			$response = new FileExplorerResponse();
			$response->error = $e->getMessage();
			return $response;
		}
	}

	/**
	 *
	 * @param  $path 
	 * @param  $filter 
	 * @param  $searchString 
	 * @param  $caseSensitive 
	 * @param  $selectedItems 
	 */
	function Search($path, $filter, $searchString, $caseSensitive, $selectedItems = null)
	{        
		try{
			$path = $this->GetPhysicalPath($this->ToAbsolute($path));
			$this->rootURL = $path;
			$response = new FileExplorerResponse();
			$this->directoryContent = array();
			if($searchString[0] == "*" && substr( $searchString, -1 ) == "*"){				
					$searchString[0] = "/";				
					$searchString[strlen($searchString)-1] = "/";
			}
			else{
				$searchString = "/" . $searchString . "/";
			}
			$searchString = str_replace("*", ".*", $searchString);
			$searchString = str_replace("?", ".?", $searchString);
			if(!$caseSensitive){
				$searchString = $searchString . "i";
			}
			if($this->IsSharedServer($path))
			return $this->SearchSharedDrive(path, searchString, caseSensitive);
			else{
				$this->GetFolderFiles($path, $searchString);
			}
			$response->files=  $this->directoryContent;
			return $response;
		}
		catch(Exception $e) {
			$response->error = $e->getMessage();
			return $response;
		}
	}
	
	function SearchSharedDrive($path, $searchString, $caseSensitive){
		return "";
	}   

	function GetFolderFiles($dir, $searchString){
		$files= array_diff(scandir($dir), array('..', '.'));
		foreach ($files as $filename) {
			$fullName= $dir . DIRECTORY_SEPARATOR . $filename;
			$preventAdd = false;
			$isFile = is_file($fullName);
			if(($isFile && ($this->ExtensionsAllow != null && $this->ExtensionsAllow != "*" && $this->ExtensionsAllow != "*.*") && !(strpos($this->ExtensionsAllow, pathinfo($fullName, PATHINFO_EXTENSION)) !== false) ) || !preg_match($searchString, $filename)){
				$preventAdd = true;
			}
			if(!$preventAdd){
				$filedetails = new FileExplorerDirectoryContent();
				$filedetails->name = $filename;
				$filedetails->type = $isFile ? "File" : "Directory";
				$filedetails->isFile = $isFile;
				$filedetails->hasChild = $isFile ? false : count(glob($fullName. "/*", GLOB_ONLYDIR))  > 0;
				$filedetails->size= $isFile ? filesize($fullName) : "";
				$filedetails->dateModified = date("F d Y H:i:s.", filemtime($fullName));
				$filedetails->filterPath= trim(str_replace($this->rootURL, " " , $dir ). DIRECTORY_SEPARATOR);
				array_push($this->directoryContent, $filedetails);
			}
			if(!$isFile)
			$this->GetFolderFiles($fullName, $searchString);
		}
	}
	
	#endregion
}

class FileExplorerResponse{
	public $cwd="";
	public $files;
	public $details;
	public $error;   
}

class FileExplorerDirectoryContent{
	public $name;
	public $type;
	public $size;
	public $dateModified;
	public $hasChild;
	public $isFile;
	public $filterPath;
	public $permission;
}
class FileDetails {
	public $Name;
	public $Location;
	public $Type;
	public $Size;
	public $Created;
	public $Modified;
	public $Permission;
}
class ImageSize
{
	public $Height;
	public $Width;
}

?>