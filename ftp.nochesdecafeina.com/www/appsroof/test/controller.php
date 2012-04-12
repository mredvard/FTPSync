<?php
	include "./model.php";
	include "./view.php";
		
	if (isset($_GET["direccion"])) {
		$email = getEmail($_POST["direccion"]);
		show_email($email);				
	} else {
		$email = getEmailList();
		show_email($email);			
	}
?>
