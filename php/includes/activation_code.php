
<?php
function generate_activation_code($base_t) {
    for ($j = -100; $j <=50; $j++) {
        srand($base_t+$j);
        echo($base_t+$j);
        echo("\n");
        $chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890";
        $activation_code = "";
        for ($i = 0; $i < 32; $i++) {
            $activation_code = $activation_code . $chars[rand(0, strlen($chars) - 1)];
        }
        echo($activation_code);
        echo("\n");
    }
}
generate_activation_code($argv[1]);
?> 
