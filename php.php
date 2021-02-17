<?php

// Placeholder
$output = NULL;

if(isset($_POST['submit'])){
    // Connect to db
    $mysqli = NEW MySQLi('127.0.0.1','root', 'budget');
    $in_id = $_POST['in_id'];
    $income = "income";
    $in_type = $_POST['in_type'];
    $in_amount = $_POST['in_amount'];
    $in_date = $_POST['in_date'];

    foreach($in_id AS $key => $value){
        $query = "SELECT * FROM budget 
                  WHERE in_id = '" . $mysqli->real_escape_string($key['in_id']) . "'";
    
        $resultSet = $mysqli->query($query);

        if($resultSet->num_rows == 0){
            // Perform insert
        }else{
            $output .= "You've already set your budget day." . $mysqli->error;
        }
            
    }
    $mysqli->close();
}

?>