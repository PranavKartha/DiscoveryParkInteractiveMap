<?php


$IPattern = $_POST['IPattern'];
$Transportation = $_POST['Transportation'];
$Visited = $_POST['Visited'];
echo $IPattern;
echo $Transportation;
echo $Visited;
//Database connection

$conn = new mysqli('localhost','root','','patterns2');
if($conn->connect_error){
	die('Connection Failed:' .$conn->connect_error);
}else{
	echo "connection sucess!";
	$stmt = $conn->prepare("insert into patterns(pattern, transtype, area) 
			values(?,?,?)");
	$stmt ->bind_param("sss",$IPattern, $Transportation, $Visited);
	$stmt->execute();
	echo "data insert successful!";

}	
//}else{
	//$stmt = $conn->prepare("insert into patternstest(Pattern)values(?)");
	//$stmt ->bind_param("s",$patternbox)
	//$stmt->execute();
	//echo "data insert successful!"
	//$stmt ->close
	//$conn->close
//}	

?>