<?php 

	// connect to the database
    $conn = mysqli_connect($user='root', $host='localhost', $port='3306', $database='budget');

	// check connection
	if(!$conn){
		echo 'Connection error: '. mysqli_connect_error();
	}

?>