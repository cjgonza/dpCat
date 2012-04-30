<?php

require_once('../includes/common.php');

/**
 * This file is used to uninstall "dpCat"
 *
 * ¡Ojo! Este código es un engaño, las modificaciones de la base de datos por
 * medio de scripts de instalación por parte de los plugins no funciona, tuve
 * que hacer estas consultas a mano en el SGBD.
 *
 */

function uninstall_dpcat()
{
	global $db;
	$db->Execute("ALTER TABLE `".tbl('video')."` DROP `license` ");
}

uninstall_dpcat();

?>
