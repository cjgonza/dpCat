<?php

require_once('../../includes/common.php');

// Se autentica contra el ClipBucket.
global $cbvideo, $userquery;
if ($userquery->login_user($_POST['user'], $_POST['pass'])) $userquery->is_login = true;

// Borra el vídeo.
$cbvideo->delete_video($_POST['vid']);

// Devuelve los posibles errrores al dpCat.
global $eh;
echo json_encode(array('cb_errors' => $eh->error_list));
?>
