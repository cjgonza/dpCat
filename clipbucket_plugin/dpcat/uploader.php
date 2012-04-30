<?php

require_once('../../includes/common.php');
require_once('dpcat.php');

// Función que detiene la ejecución y devuelve la información al dpCat.
function return_and_exit($message = null) {
    global $eh, $vlink, $vid;
    $data = array(
        'message' => $message,
        'cb_errors' => $eh->error_list,
        'vlink' => $vlink,
        'vid' => $vid
    );
    echo json_encode($data);
    exit();
}

// Se autentica contra el ClipBucket.
global $cbvideo, $userquery;
if ($userquery->login_user($_POST['user'], $_POST['pass'])) $userquery->is_login = true;

// Prepara la información sobre el vídeo a publicar.
$file_key = time() . RandomString(5);
$file_src = $_POST['file'];
$array = array(
    'title' => $_POST['title'],
    'description' => $_POST['description'],
    'tags' => $_POST['tags'],
    'category' => array($_POST['category']),
    'file_name' => $file_key,
    'userid' => $userquery->userid,
);

// Se le envía al ClipBucket los datos del vídeo.
$upl = new Upload();
$vid = $upl->submit_upload($array);

// Datos aceptados, se copia el vídeo y se inserta en la cola de procesado.
if ($vid) {
    $base_name = $file_key . '.' . getExt($file_src);
    $file_name = TEMP_DIR . '/' . $base_name;
    if (!copy($file_src, $file_name)) {
        $cbvideo->delete_video($vid);
        @unlink($file_name);
        return_and_exit("Error al copiar el fichero");
    }
    $upl->add_conversion_queue($base_name);
    set_license_data($vid, $_POST['license']);
    $vlink = video_link($vid);
    return_and_exit();
}

// Error: No se pudo publicar el vídeo.
return_and_exit();

?>
