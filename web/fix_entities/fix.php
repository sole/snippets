<?php

/*

Reads text from the txt.txt file and fixes entities and a couple other
things into the new txt.txt file.

*/

$replacements = array(
	'&aacute;' => 'á',
	'&eacute;' => 'é',
	'&iacute;' => 'í',
	'&oacute;' => 'ó',
	'&uacute;' => 'ú',
	'&ntilde;' => 'ñ',
	'&iexcl;'  => '¡',
	'<br /> '  => "\n",
	'<br />'  => "\n",
	'&uuml;'   => 'ü',
	'&iquest;' => '¿',
	'&ograve;' => 'ò',
	'&Eacute;' => 'É',
	'&Iacute;' => 'Í',
	'&quot;' => '"'
);

$txt = file_get_contents('txt.txt');

$txt = str_replace(array_keys($replacements), array_values($replacements), $txt);

file_put_contents('txt.txt', $txt);

?>
