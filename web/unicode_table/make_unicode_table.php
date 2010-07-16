<!DOCTYPE html> 
<html lang="en"> 
	<head> 
		<meta charset="utf-8"> 
		<title>unicode table</title>
	</head>
	<body>
	
	<p>A server-side generated unicode table will appear below this text.</p>
		
	<?php
	$row_length = 20;
	echo '<table>';
	$current_row_count = 0;
	for($i = 0; $i < 2000; $i++)
	{
		if($current_row_count == 0) {
			echo '<tr>';
		}
		
		echo '<td class="code">' . $i . '</td><td class="character"> &#' . $i . '</td>';
		
		$current_row_count++;
		
		if($current_row_count % $row_length == 0) {
			echo '</tr>';
			$current_row_count = 0;
		}
	}
	echo '</table>';
	?>
	<style type="text/css">
		table { border: 1px solid #ccc; border-collapse: collapse; }
		td { padding: 5px 3px; border: 1px dotted #ddd; border-width: 0px 1px 2px 0px; border-bottom-style: solid; }
		tr:nth-child(even) { background: #f8f8f8; }

	<style>
	</body>
</html>
