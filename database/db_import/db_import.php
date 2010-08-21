<html>
<head><title>migrate!</title></head>
<body>
<style type="text/css">.error{font-weight: bold; color:#900;}</style>
<?php
require_once('config.php');
require_once('tables.php');

$t_start = time();

$db_src = new Database($config['database']['source']);
$db_dst = new Database($config['database']['destination']);

foreach($tables as $table) {
	$src_fields = $db_src->get_table_fields($table['source']);
	$excluded = isset($table['exclude']) ? explode(",", $table['exclude']) : array();
	$included = isset($table['include']) ? explode(",", $table['include']) : array();
	if(count($excluded)>0 && count($included)>0) {
		ER("Error in $table: both included and excluded fields at the same time. Skipping.");
		continue;
	} else if(count($excluded)>0) {
		$mode = "excluding";
	} else if(count($included)>0) {
		$mode = "including";
	}

	$dst_fields = array();
	foreach($src_fields as $name => $field) {
		if($mode=="excluding" && in_array($name, $excluded)) {
			continue;
		} else if($mode=="including" && !in_array($name, $included)) {
			continue;
		}
		if(isset($table['map']) && array_key_exists($name, $table['map'])) {
			$dst_name = $table['map'][$name];
			$field['src_name'] = $name; 
		} else {
			$dst_name = $name;
		}
		$dst_fields[$dst_name] = $field;
	}
	
	$table_info =
		array(
			"name"		=> $table['destination'],
			"fields"	=> $dst_fields
		);

	$update_mode = $db_dst->table_exists($table_info['name']);
	$res = $db_dst->process_table($table_info);
	if($res!=false) {
		$first_field = array_shift(array_keys($src_fields));
		$query = "SELECT * FROM {$db_src->name}.$table[source] ORDER BY $first_field ASC";
		$res = mysql_query($query, $db_src->dbh);
		while($row = mysql_fetch_assoc($res)) {
			if(!$update_mode) {
				$q_insert = "INSERT INTO {$db_dst->name}.$table[destination] ";
				$pairs = get_field_pairs($dst_fields, $row);
				$columns = implode(",", array_keys($pairs));
				$values = implode(",", array_values($pairs));
				$q_insert .= "($columns) VALUES ($values);";
				$res_insert = mysql_query($q_insert);
				if(!$res_insert) {
					ER($res_insert.": ".mysql_error());
				}
			} else {
				$q_update = "UPDATE {$db_dst->name}.$table[destination] SET ";
				$pairs = get_field_pairs($dst_fields, $row);
				$sql_pairs = array();
				foreach($pairs as $field=>$value) {
					$sql_pairs[] = " $field = $value";
				}
				$q_update.= implode(", ", $sql_pairs);
				$q_update.= " WHERE id='".$row[$table['use_key']]."'";
				$res_update = mysql_query($q_update);
				if(!$res_update) {
					ER($res_update.": ".mysql_error());
				}
			}
		}
	}
}

$t_total = time() - $t_start;
echo "$t_total seconds!!";

function get_field_pairs($dst_fields, $row) {
	$pairs = array();
	foreach($dst_fields as $name=>$field) {
		if(isset($row[$name])) {
			$value = "'".addslashes($row[$name])."'";
		} else if (isset($row[$field['src_name']])) {
			$value = "'".addslashes($row[$field['src_name']])."'";
		} else {
			continue;
		}
		$pairs["`$name`"] = $value;
	}
	return $pairs;
}

class Database {
	var $dbh;
	var $name;

	function Database($db_config) {
		$f = $db_config['connect'];
		$this->dbh = $f($db_config['server'], $db_config['login'], $db_config['password']);
		$this->name = $db_config['database'];
	}

	function get_table_fields($table) {
		// do a show fields, return associative array
		$query = "SHOW FIELDS FROM {$this->name}.$table";
		$res = mysql_query($query, $this->dbh);
		$fields = array();
		while($row = mysql_fetch_assoc($res)) {
			$name = $row['Field'];
			$fields[$name]['type'] = $row['Type'];
			$fields[$name]['null'] = $row['Null']=="YES" ? true : false;
			$fields[$name]['key'] = !empty($row['Key']) ? $row['Key'] : null;
			$fields[$name]['default'] = isset($row['Default']) ? $row['Default'] : null;
			$fields[$name]['extra'] = !empty($row['Extra']) ? $row['Extra'] : null;
		}
		return $fields;
	}

	/**
	 * take care of creating or updating the table structure (depending on the table previously existing or not)
	 */
	function process_table($table_info) {
		print_r($table_info);echo "<hr />";
		if($this->table_exists($table_info['name'])) {
			$query = "ALTER TABLE {$this->name}.`$table_info[name]`";
		} else {
			$query = "CREATE TABLE {$this->name}.`$table_info[name]` ("; 
			$create = true;
		}

		$columns = array();
		$keys = array();
		foreach($table_info['fields'] as $name => $field) {
			$column = "\n\t";
			if(!$create) {
				$column .= "ADD COLUMN ";
			}
			$column .= "`$name` $field[type]";
			if(!$field['null'])
				$column .= " NOT NULL";
			if(!is_null($field['extra']))
				$column .= " $field[extra]";
			if(!is_null($field['default']))
				$column .= " default '$field[default]'";
			else
				$column .= " default NULL";
			$columns [] = $column;

			if(isset($field['key'])) {
				$keys[$field['key']][] = $name;
			}
		}

		$query .= implode(",", $columns);

		$constraints = array();
		foreach($keys as $key=>$keyfields) {
			for($i=0; $i<count($keyfields); $i++) {
				$keyfields[$i] = "`".$keyfields[$i]."`";
			}
			$keytext = implode(",", $keyfields);
			if($key=="PRI") {
				$constraints[$key] = "PRIMARY KEY($keytext)";
			} else if($key=="UNI") {
				$constraints[$key] = "UNIQUE($keytext)";
			}
			if(!$create) {
				$constraints[$key] = "ADD ".$constraints[$key];
			}
		}
		if(count($constraints)>0) {
			$query.= ",\n".implode(",\n", $constraints);
		}
		
		if($create) {
			$query .="\n)";
		}
		echo "<pre>$query</pre>";
		$res = mysql_query($query, $this->dbh);
		if($res == false) {
			ER(mysql_error());
		} else {
			OK("processed");
		}
		return $res;
	}
	
	function table_exists($table) {
		if (mysql_query("SELECT 1 FROM ".$this->name.".`".$table."` LIMIT 0", $this->dbh)) {
			return true;
		} else {
			return false;
		}
	}
}

function OK($text) {
	echo "<p>$text</p>";
}

function ER($text) {
	echo "<p class=\"error\">$text</p>";
}
?>
</body>
</html>