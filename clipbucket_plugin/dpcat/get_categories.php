<?php
require_once('../../includes/common.php');

global $cbvid;
echo json_encode($cbvid->get_categories());
?>
