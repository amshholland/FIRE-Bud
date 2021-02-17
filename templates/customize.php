<?php

// Placeholder
$output = NULL;

if(isset($_POST["submit"])){
    // Connect to db
    $mysqli = NEW MySQLi($user='budget_ash', $password='HarryP&tSS1', $host='127.0.0.1', $port='3306', $database='budget');
    $id = $mysqli -> $_POST['id'];
    $day = $mysqli->real_escape_string($_POST['day']);
    $in_id = $_POST['in_id'];
    $income = "income";
    $in_type = $_POST['in_type'];
    $in_amount = $_POST['in_amount'];
    $in_date = $_POST['in_date'];

    echo $_POST['id'];
    echo $_POST['day'];
    echo $day;
    echo $in_id;

    $sql = "UPDATE users SET budget_day = ($day) WHERE id = ($id)";

    // foreach($in_id AS $value => $key){
    if($mysqli -> query($sql) == TRUE){
        printf("Row inserted.\n");
    }else{
        printf("failed.");
    }
$mysqli->close();
}

?>