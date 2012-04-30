<?php
/*
	Plugin Name: dpCat
	Description: Conector con el servidor dpCat.
	Author: Pablo Chinea
	ClipBucket Version: 2
	Plugin Version: 2.0
	Website: http://dpcat.es/
*/

include("license_code.php");

function set_license_data($vid, $license) {
    global $db;
    $db->update(tbl("video"), array("license"), array($license), " videoid='$vid'");
}

function print_license_tag($data) {
    global $license_code;
    echo '<div class="license-box"><ul>';
    echo '<li>Licencia: </li>';
    echo '<li>'.$license_code[$data['license']].'</li>';
    echo '</ul></div>';
}

register_anchor_function('print_license_tag', "license_tag");
