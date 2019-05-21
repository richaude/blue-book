<!DOCTYPE html>
<html> 
<head>
	<meta charset="UTF-8" />
	<title>Php interaktiv mit Python</title> 
</head>
 
<body>
<h1>Daten in Python schmeißen und wieder herausbekommen</h1>

<p>Im folgenden wird die Zeichenkette "world" in ein Python Skript namens phpTry.py gegeben. Dies soll die Query als Eingabe darstellen: 
<?php
// $python = `python phpTry.py "world"`;
$python = exec('python phpTry.py "world"', $output, $ret_code);
echo $python;
//echo $ret_code;
?></p>
<p>Anscheinend werden Print Statements in Python als Strings in der Variablen $python gespeichert.</p>
 
</body>
</html>
