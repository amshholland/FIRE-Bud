// MySQLi Procedural

<?php
include('config/db_connect.php');

$errors = array('day' => ''); 

if (isset($_POST['submit'])){
    // Check for budget day
    if(empty($_POST['day'])){
        $errors['day'] = "Please provide which day of the month you'd like to set your budget day as.";
    }else{
        $day = $_POST['day'];
    }

    if(array_filter($errors)){
        // Echo 'errors in form';
    }else{
        
        $day = mysqli_real_escape_string($conn, $_POST['day']);
        $id = mysqli_real_escape_string($conn, $_POST['id']);

        // Create sql
        $sql = "UPDATE users SET budget_day = ('$day') WHERE id = ('$id')";

        // Save to db & check
        if(mysqli_query($conn, $sql)){
            // Success
            header "index.html";
        }else{
            // Error
            echo 'query error: '. mysqli_error($conn);
        }
    }
}
?>