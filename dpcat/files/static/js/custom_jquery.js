

// Hacer desaparecer los mensajes tipo.

$(document).ready(function() {
    $(".cerrar").click(function () {
        $(this.parentNode).animate({ opacity: 0, height: 0 }, "slow").hide("slow");
    });
});
