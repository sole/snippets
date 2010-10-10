<?php

$tmp_dir = dirname(__FILE__) . '/tmp';

$spanish_url = 'http://es.wikipedia.org/wiki/ISO_3166-1';
$spanish_file = $tmp_dir . '/es.html';

$english_url = 'http://www.iso.org/iso/list-en1-semic-2.txt';
$english_file = $tmp_dir . '/en.txt';

$select_es = $tmp_dir . '/select_es.txt';
$select_en = $tmp_dir . '/select_en.txt';

$php_en = $tmp_dir . '/php_en.inc';
$php_es = $tmp_dir . '/php_es.inc';

if(!file_exists($tmp_dir))
{
	mkdir($tmp_dir);
}

if(!file_exists($spanish_file))
{
	file_put_contents($spanish_file, file_get_contents($spanish_url));
}

if(!file_exists($english_file))
{
	file_put_contents($english_file, file_get_contents($english_url));
}

$countries = array();

// Spanish ---------------------

$text = file_get_contents($spanish_file);

// segmentation fault with preg_match_all
// we'll use an slightly slower method which works

$lines = explode("\n", $text);

$buffer = array();

foreach($lines as $line)
{
	$t = trim($line);
	if($t == '<pre>')
	{
		$block = array();
	}
	else if($t == '</pre>')
	{
		$buffer = array_merge($buffer, $block);
	}
	else
	{
		$block[] = $t;
	}
}

foreach($buffer as $line)
{
	preg_match('@(.{3}) (\w{3}) (\w{2}) (-{12}|<a.*?/a>) (<span class="flagicon">)?(<a.*?/a>) (</span>)?<a.*?>(.+?)</a>@', $line, $matches);

	$num_code = trim($matches[1]);
	$code = trim(strtolower($matches[3]));
	$country = $matches[8];

	if($num_code == '---') continue;
	
	if(strlen($code) > 0)
	{
		$countries[$code] = array('es' => $country);
	}
}

// English ----------------

$text = file_get_contents($english_file);

$lines = explode("\n", $text);

// The first two lines are useless
unset($lines[0]);
unset($lines[1]);

foreach($lines as $line)
{
	list($country, $code) = explode(";", $line);
	$country = ucwords(strtolower($country));
	$code = trim(strtolower($code));

	if(strlen($code) > 0)
	{
		$countries[$code]['en'] = $country;
	}
}

echo 'done';

$countries_es = array();
$countries_en = array();

foreach($countries as $code => $country)
{
	if(array_key_exists('es', $country) && array_key_exists('en', $country))
	{
		$countries_es[$code] = $country['es'];
		$countries_en[$code] = $country['en'];
	}
}

asort($countries_es);
asort($countries_en);

function make_select($countries)
{
	$out = '<select name="country">';
	foreach($countries as $code => $country)
	{
		$out .= sprintf("\t" . '<option value="%s">%s</option>' . "\n", $code, $country);
	}
	$out .= '</select>';
	
	return $out;
}

function make_php_array($countries)
{
	$out = 'array(';
	
	foreach($countries as $code => $country)
	{
		$out .= sprintf("\t'%s'\t=>\t'%s',\n", $code, $country);
	}
	
	$out.= ');';
	
	return $out;
}

//-----------------------------

$out_es = make_select($countries_es);
$out_en = make_select($countries_en);

file_put_contents($select_es, $out_es);
file_put_contents($select_en, $out_en);

file_put_contents($php_es, make_php_array($countries_es));
file_put_contents($php_en, make_php_array($countries_en));

?>
