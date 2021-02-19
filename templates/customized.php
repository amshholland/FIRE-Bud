<?php

$hostname = '127.0.0.1:3306';
$username = 'root';
$database = 'budget';
$pw = '123';

// Connect to db
$conn = NEW MySQLi($hostname, $username, $pw, $database);
if ($conn->connect_errno) {
    printf("Connect failed: %s\n", $conn->connect_error);
    exit();
}

// Placeholder
$output = NULL;

if(isset($_POST['submit'])){
    $id = $_POST['id'];
    $day = $_POST['day'];
    // $in_id = $_POST['in_id'];
    // $income = "income";
    // $in_type = $_POST['in_type'];
    // $in_amount = $_POST['in_amount'];
    // $in_date = $_POST['in_date'];

    $stmt = $conn -> prepare("UPDATE users SET budget_day = (?) WHERE id = (?)");
    $stmt->bind_param('ii', $day, $id);
    $stmt->execute();
    
    // foreach($in_id AS $value => $key){
    if($stmt->execute() == TRUE){
        $row_count = $stmt -> num_rows;
        printf("%d Row inserted.\n", $row_count);
    }else{
        printf("failed.");
    }
$conn->close();
}

?>