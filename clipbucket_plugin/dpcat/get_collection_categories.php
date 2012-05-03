<?php
require_once('../../includes/common.php');

global $cbcollection;
echo json_encode($cbcollection->get_categories());
?>
