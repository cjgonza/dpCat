<?php
require_once('../../includes/common.php');

$data = get_collections(null);
if (!$data)
    $data = Array();

echo json_encode($data);
?>
