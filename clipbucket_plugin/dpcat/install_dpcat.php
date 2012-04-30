<?php

require_once('../includes/common.php');

/**
 * This file is used to install "dpCat"
 *
 * ¡Ojo! Este código es un engaño, las modificaciones de la base de datos por
 * medio de scripts de instalación por parte de los plugins no funciona, tuve
 * que hacer estas consultas a mano en el SGBD.
 *
 */

function install_dpcat()
{
	global $db;
	$db->Execute("ALTER TABLE `".tbl('video')."` ADD `license` VARCHAR(2) NOT NULL ");
}

install_dpcat();

?>
