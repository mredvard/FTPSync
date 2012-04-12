<?php
	function getEmail($email) {
		$con = mysql_connect("localhost","nochesde_apps","Holashit2010!");		
		mysql_select_db("nochesde_appsroof",$con);
		$sql="SELECT * FROM correos WHERE direccion='$email'";
		$result=mysql_query($sql);
		$count=0;		
		while ($item=mysql_fetch_array($result)){
			$emailArray[$count] = $item['direccion'];
			$count=$count+1;
		}
		mysql_close($con);
		return $emailArray;	
	}
	function getEmailList() {
		$con = mysql_connect("localhost","nochesde_apps","Holashit2010!");
		mysql_select_db("nochesde_appsroof",$con);
		$sql="SELECT * FROM correos";
		$result=mysql_query($sql);
		$count=0;		
		while ($item=mysql_fetch_array($result)){
			$emailArray[$count] = $item['direccion'];
			$count=$count+1;
		}
		mysql_close($con);
		return $emailArray;
	}
?> 
