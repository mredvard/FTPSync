<?php
	function spamcheck($field) {
		//filter_var() sanitizes the e-mail
		//address using FILTER_SANITIZE_EMAIL
		$field=filter_var($field, FILTER_SANITIZE_EMAIL);
		
		//filter_var() validates the e-mail
		//address using FILTER_VALIDATE_EMAIL
		if(filter_var($field, FILTER_VALIDATE_EMAIL)) {
			return TRUE;
		} else {
			return FALSE;
		}
	}
	
	function buscar_duplicado($field,$db) {
		mysql_select_db("nochesde_appsroof",$db);
		$sql="SELECT direccion FROM correos WHERE direccion='$field'";
		$resultado = mysql_query($sql,$db);
		if (!$resultado) {
    		die('Invalid query: ' . mysql_error());
		}
		if (mysql_num_rows($resultado) == 0) {
			return FALSE;	
		} else {
			return TRUE;
		}
	}
 /*Fin de la funcion*/
 	$mensaje="Hey there!, thanks for signing up for AppsRoof!

We’ll offer the best deals in mobile apps you’ll ever see!, and don’t worry, you’ll hear from us very soon, so keep your eyes open,  follow us on Twitter (@AppsRoof) and check out our Facebook page (http://www.facebook.com/pages/AppsRoofcom/259538910741073).

Best regards, 

Edgar
AppsRoof Founder";
	/*$headers = "Message-ID:<".$now." TheSystem@".$_SERVER['SERVER_NAME'].">"."\r\n"; 
	$headers .= "X-Mailer: PHP v".phpversion()."\r\n";   
	$headers .= 'MIME-Version: 1.0' . "\r\n";
	$headers .= 'Content-type: text/html; charset=iso-8859-1' . "\r\n";*/
	$headers = 'From: Edgar Contreras <edgar@appsroof.com>';
  
	$email=$_POST['email'];
	if (preg_match('/^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/',$email)) {
		$con = mysql_connect("localhost","nochesde_apps","Holashit2010!");
		if (!$con) {
			die('Could not connect: ' . mysql_error());
		}
		$mailcheck = spamcheck($email);
		$repetido = buscar_duplicado($email,$con);
		if ($mailcheck and $repetido == FALSE) {
			mysql_select_db("nochesde_appsroof",$con);
	
			$sql= "INSERT INTO correos
					VALUES ('$email')";
			if (!mysql_query($sql)) {
				die('could not add new email: ' . mysql_error());	
			}
			mail($email, "AppsRoof.com confirmation",$mensaje, $headers );
		}
		mysql_close($con);
	}
	else {
		return false;
	}
?>