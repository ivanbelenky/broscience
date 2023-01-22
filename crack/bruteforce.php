<?php
function check_hash($hash, $hash_to_crack, $word){
    if($hash == $hash_to_crack){
        echo "The password is: ".$word;
        exit;
    };
};

function print_progress($counter){
    if ($counter % 10000 == 0) {
        echo "Tried ".$counter." word combinations\n";
    };
};

if(count($argv) != 4){
    echo("Usage: php bruteforce.php <hash_to_crack> <db_salt> <wordlist>");
    exit;
};

$hash_to_crack = $argv[1];
$db_salt = $argv[2];
$wordlist = $argv[3];


$file = fopen($wordlist, "r");
while(! feof($file)){    
    $words[] = fgets($file);
}
fclose($file);

$counter = 0;    
foreach($words as $word){
    $word = trim($word);
    $hash = md5($db_salt . $word);
    check_hash($hash, $hash_to_crack, $word);
    $counter++;
    print_progress($counter);
}
echo "Tried all (".$counter.") single word combinations";

?>
