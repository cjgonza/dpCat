<?php

// Indica al ClipBucket que se trata de una operación en background (no enviada
// desde el navegador), debe hacerse antes de incluir el ClipBucket.
$in_bg_cron = true;

include("{{ cb_path}}/includes/config.inc.php");

global $cbvid;
echo json_encode($cbvid->get_categories());
?>
