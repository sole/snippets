<?php
$tables  = array();

$tables[] =
	array(
		'source'	=>	'user',
		'destination'=>	'users',
		'map' =>
			array(
				"user_id"	=>	"id",
				"firstname"	=>	"first_name",
				"lastname"	=>	"last_name"
			),
		'exclude' => "type,flagged,address_id,shipping_address_id,billing_address_id,shiptobilling,from_site_id,pluginz_user_id,jahshaka_user_id,avatar,dob,upload_quota,uploaded_amount,deleted,deleted_date,frontpage"
	);
	
$tables[] =
	array(
		'source'	=>	'user_details',
		'destination'=>	'users',
		'include' => "homepage,interests,movies,music,skills,role,industry,motto,loc_city,loc_country,user_description,last_updated,profile_viewed",
		'use_key' => "user_id"
	);
	
$tables[] =
	array(
		'source'	=>	'user_info',
		'destination'=>	'users',
		'map' =>
			array(
				'account_created' => "created",
				'last_modified'	=>	"modified"
			),
		'include' => "account_created,last_modified",
		'use_key' => "user_id"
	);

$tables[] =
	array(
		'source'	=>	'asset',
		'destination'=>	'assets',
		'map' =>
			array(
				"asset_id"	=>	"id",
				"lastname"	=>	"last_name"
			),
		'exclude' => "GUID,folder"
	);

?>