<?php
$config = array(
	"database"	=> array(
		'source' => array(	'driver'     => 'mysql',
							'connect'    => 'mysql_connect',
							'host'       => 'localhost',
							'login'      => 'sole',
							'password'   => 'notocar',
							'database'   => 'jahnet_v2',
							'prefix'     => ''),
		'destination' => array(	'driver' => 'mysql',
							'connect'    => 'mysql_connect',
							'host'       => 'localhost',
							'login'      => 'sole',
							'password'   => 'notocar',
							'database'   => 'jahnet_cake',
							'prefix'     => '')
	)
);
?>
