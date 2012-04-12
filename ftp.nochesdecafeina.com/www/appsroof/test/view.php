<?php
	function show_email($email) {
		echo "<table id='data'>";
		echo "<tr>";
		echo "<td class='data_header'>Direcciones</td>";
		echo "</tr>";
		$size=sizeof($email);
		if ($size>0) { 
			foreach($email as $i) {
				echo "<tr>";
				echo "<td>$i</td>";
				echo "</tr>";
			}
		} else {
			echo "<tr>";
			echo "<td>$email</td>";
			echo "</tr>";
		}
		echo "</table>";
	}
?>
