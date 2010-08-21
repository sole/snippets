Script for importing and transforming databases
-----------------------------------------------

1. Configuration
2. Use it!


1. Configuration
=================

There are two files you need to alter appropiately:

a) config.php

There's the definition of the source and destination databases. The syntax is the same than cake php's one.

You can also use the same database as source and destination - but horrible things may happen if there are overlappings between table names. This has not been tested.

b) tables.php

Here you specify the tables you want to move, with the modifications required:

Create an entry in $tables for each table in the source database that you want to process. This is the meaning of each parameter:

- source: table name in the source database

- destination: table name in the destination database

- map: array containing field names in the source database and their correspondence in the destination one. This is how field names are renamed. For example, you can map fname to first_name with $map = array('fname' => 'first_name');

- exclude: comma separated list of fields you do not want to include when copying the table
- include: comma separated list of fields you want to include when copying the table

Please note that you can't specify exclude and include at the same time. Doing so will result in the table being skipped.

The way it works depends on if 'exclude' or 'include' are specified.
If 'exclude' is specified, the script will include all the fields excluding the specified ones.
If 'include' is specified, the script will include only the specified fields.

For example, if you need to discard more fields than the ones you want to keep, you'll use only include, avoiding a long "exclude" list.

- use_key: this is only used when you need to add data from one table into an existing one, i.e. merging two tables. Specify with this the name of the source table which represents the "id" in the destination table.

Example:

You have two tables that you want to merge in just one, user and user_details:
user (user_id, name, firstname, etc...)
user_details (user_id, homepage, motto, etc...)


In this case $tables will look like this ([...] means there's more irrelevant data:

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
		'exclude' => "type,flagged [...]"
	);
	
$tables[] =
	array(
		'source'	=>	'user_details',
		'destination'=>	'users',
		'include' => "homepage",
		'use_key' => 'user_id'
	);
	
Note how the main table users is created with the data of user table, and then the data from user_details is merged into users by specifying the destination table 'users' and the key 'user_id'.

What the script does is detect the table already exist and then instead of generating series of INSERT's, it does generate UPDATE's and adding a "WHERE id = " and the value in the second table of the key you specified. In this case it would be using the value of user_details.user_id, since it's a 1:1 correspondence.

2. Use it
===========

For using this script, place all the files of the db_import folder inside the webroot - so that it can be accessed via a web browser. For example: http://localhost/db_import/db_import.php
If there are errors they will be output. In that case it may be worth to delete all the created tables, fix the errors and re-run the script again.
