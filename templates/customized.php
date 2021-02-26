{% extends "layout.html" %}

{% block title %}
Customized Budget
{% endblock %}

{% block main %}

<?php

$output = NULL;

if (isset($_POST['submit'])) {

    // Connect to db
    $hostname = '127.0.0.1:3306';
    $username = 'root';
    $database = 'budget';
    $pw = '';

    $conn = mysqli_connect($hostname, $username, $pw, $database);
    if (!$conn) {
        echo ("Connect failed: %s\n" . mysqli_connect_error());
        exit();
    }

    $id = $_POST['id'];
    $day = $_POST['day'];

    if ($day != NULL) {
        $stmt = "UPDATE users SET budget_day = ('"
            . $conn->real_escape_string($day) .
            "')
            WHERE id = ('"
            . $conn->real_escape_string($id) .
            "')
            ";
        $update = $conn->query($stmt);

        if (!$update) {
            echo $conn->error;
        } else {
            $output .= '<p> Successfully added ' . $day . '</p>';
        }
    }

    // Submit income info
    $in_id = $_POST['in_id'];
    $income = $_POST['income'];
    $in_type = $_POST['in_type'];
    $in_amount = $_POST['in_amount'];
    $in_date = $_POST['in_date'];

    if ($in_type != NULL) {
        foreach ($in_id as $key => $value) {
            $stmt = "INSERT INTO budget VALUES ('"
                . $conn->real_escape_string($value) .
                "','"
                . $conn->real_escape_string($income[$key]) .
                "','"
                . $conn->real_escape_string($in_type[$key]) .
                "','"
                . $conn->real_escape_string($in_amount[$key]) .
                "','"
                . $conn->real_escape_string($in_date[$key]) .
                "')
                ";

            $insert = $conn->query($stmt);

            if (!$insert) {
                // Successfully loaded into db

                echo $conn->error;
            } // else {
            // $output .= '<p> Successfully added ' . $day . $in_type[$key] . '</p>';
        }
    }

    // Submit dynamic category info
    $ex_id = $_POST['ex_id'];
    $expense = $_POST['expense'];
    $ex_type = $_POST['ex_type'];
    $ex_amount = $_POST['ex_amount'];

    if ($ex_type != NULL) {
        foreach ($ex_id as $key => $value) {
            $stmt = "INSERT INTO budget (id, ie, category, amount) 
            VALUES ('"
                . $conn->real_escape_string($value) .
                "','"
                . $conn->real_escape_string($expense[$key]) .
                "','"
                . $conn->real_escape_string($ex_type[$key]) .
                "','"
                . $conn->real_escape_string($ex_amount[$key]) .
                "')
            ";

            $insert = $conn->query($stmt);

            if (!$insert) {
                // Successfully loaded into db
                echo $conn->error;
            } else {
                //header("Location: http://localhost/project/templates/index.html");
                // $output .= '<p> Successfully added ' . $day . $in_type[$key] . '</p>';
            }
        }
    }

    $bill_id = $_POST['bill_id'];
    $expense = $_POST['expense'];
    $bill_type = $_POST['bill_type'];
    $bill_amount = $_POST['bill_amount'];
    $bill_date = $_POST['bill_date'];

    if ($bill_type != NULL) {
        foreach ($bill_id as $key => $value) {
            $stmt = "INSERT INTO budget VALUES ('"
                . $conn->real_escape_string($value) .
                "','"
                . $conn->real_escape_string($expense[$key]) .
                "','"
                . $conn->real_escape_string($bill_type[$key]) .
                "','"
                . $conn->real_escape_string($bill_amount[$key]) .
                "','"
                . $conn->real_escape_string($bill_date[$key]) .
                "')
            ";

            $insert = $conn->query($stmt);

            if (!$insert) {
                // Successfully loaded into db
                echo $conn->error;
            } else {
                //header("Location: http://localhost/project/templates/index.html");
                // $output .= '<p> Successfully added ' . $day . $in_type[$key] . '</p>';
            }

            //$query = $conn -> prepare("SELECT * FROM budget WHERE in_id = ?");
            //$stmt->bind_param('i', $in_id);

        }
    }
    echo $output;
}
?>
{% endblock %}