<?php

	include('config/db_connect.php');

	if(isset($_POST['submit'])){

        // escape sql chars
        $day = mysqli_real_escape_string($conn, $_POST['day']);
        $in_type = mysqli_real_escape_string($conn, $_POST['in_type']);
        $in_amount = mysqli_real_escape_string($conn, $_POST['in_amount']);
        $in_date = mysqli_real_escape_string($conn, $_POST['in_date']);

        // create sql
        $sql = "INSERT INTO budget(catagory,amount,date) VALUES('$in_type','$in_amount','$in_date')";

        // save to db and check
        if(mysqli_query($conn, $sql)){
            // success
            header('Location: index.html');
        } else {
            echo 'query error: '. mysqli_error($conn);
        }

    }

	} // end POST check

?>

<!DOCTYPE html>
<html>
	
	<?php include('templates/header.php'); ?>

	<section class="container grey-text">
		<h4 class="center">Add a Pizza</h4>
		<form class="white" action="<?php echo $_SERVER['PHP_SELF'] ?>" method="POST">
			<label>Your Email</label>
			<input type="text" name="email" value="<?php echo htmlspecialchars($email) ?>">
			<div class="red-text"><?php echo $errors['email']; ?></div>
			<label>Pizza Title</label>
			<input type="text" name="title" value="<?php echo htmlspecialchars($title) ?>">
			<div class="red-text"><?php echo $errors['title']; ?></div>
			<label>Ingredients (comma separated)</label>
			<input type="text" name="ingredients" value="<?php echo htmlspecialchars($ingredients) ?>">
			<div class="red-text"><?php echo $errors['ingredients']; ?></div>
			<div class="center">
				<input type="submit" name="submit" value="Submit" class="btn brand z-depth-0">
			</div>
		</form>
	</section>

	<?php include('templates/footer.php'); ?>

</html>