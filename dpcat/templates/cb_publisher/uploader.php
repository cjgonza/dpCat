<?php

// Indica al ClipBucket que se trata de una operación en background (no enviada
// desde el navegador), debe hacerse antes de incluir el ClipBucket.
$in_bg_cron = true;

include("{{ cb_path }}/includes/config.inc.php");

// Se autentica contra el ClipBucket.
global $userquery;
$userquery->login_user("{{ auth.user }}", "{{ auth.pass }}");

// Prepara la información sobre el vídeo a publicar.
$file_key = time() . RandomString(5);
$file_src = '{{ v.fichero }}';
$array = array(
    'title' => '{{ v.metadata.title }}',
    'description' => '{{ v.metadata.description }}',
    'tags' => '{{ v.metadata.keyword }}',
    'category' => array({{ category }}),
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
    copy($file_src, $file_name);
    $upl->add_conversion_queue($base_name);
    exit(0);
}

// Error: No se pudo publicar el vídeo.
global $eh;
foreach ($eh->error_list as $err)
    echo "$err\n";
exit(1);

?>
