$(document).ready(function() {
// Checkbox generación de ticket
    function mostrarGenerarTicket() {
        if ($("input:checkbox:checked").length == 0)
            $("#generar-ticket").hide();
        else
            $("#generar-ticket").show();
    }

    mostrarGenerarTicket();

    $(".marcar-todo").click(function() {
        $(".checkbox-ticket").not(this).prop("checked", this.checked);
        mostrarGenerarTicket();
    });

    $(".checkbox-ticket").click(function() {
        if (!this.checked)
            $(".marcar-todo").prop("checked", false);
        mostrarGenerarTicket();
    });
});
