<?php

$hostname = '127.0.0.1:3306';
$username = 'root';
$database = 'budget';
$pw = '';

// connect to the database
$conn = mysqli_connect($hostname, $username, $pw, $database);

// check connection
if (!$conn) {
	echo ("Connect failed: %s\n" . mysqli_connect_error());
	exit();
}