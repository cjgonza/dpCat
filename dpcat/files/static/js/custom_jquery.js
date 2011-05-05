

// Hacer desaparecer los mensajes tipo.

$(document).ready(function() {
    $(".cerrar-amarillo").click(function () {
        $(".mensaje.amarillo").fadeOut("slow");
    });
    $(".cerrar-rojo").click(function () {
        $(".mensaje.rojo").fadeOut("slow");
    });
    $(".cerrar-azul").click(function () {
        $(".mensaje.azul").fadeOut("slow");
    });
    $(".cerrar-verde").click(function () {
        $(".mensaje.verde").fadeOut("slow");
    });
});
