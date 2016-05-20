$(document).ready(function() {
// Checkbox generación de ticket
    function mostrarGenerarTicket() {
        if ($("input:checkbox:checked").length == 0){
            $("#generar-ticket").hide();
            $("#archivar").hide();
        }else{
            $("#generar-ticket").show();
            $("#archivar").show();
        }
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

    $("#terminos").click(function(e) {
        if (!$("#accept_terms")[0].checked) {
            e.preventDefault();
            $("#dialog-terminos").modal();
        }
    });

    $(function(){
        //inicializar select2
        $(".select2").select2();

        //Date picker
        $('#from').datepicker({
          autoclose: true, format: 'dd/mm/yyyy'
        });
        $('#to').datepicker({
          autoclose: true, format: 'dd/mm/yyyy'
        });
        //iCheck for checkbox and radio inputs
        $('input[type="checkbox"].minimal, input[type="radio"].minimal').iCheck({
          checkboxClass: 'icheckbox_minimal-blue',
          radioClass: 'iradio_minimal-blue'
        });
        //Flat red color scheme for iCheck
        $('input[type="checkbox"].flat-red').iCheck({
          checkboxClass: 'icheckbox_flat-green'
        });

        $('#example').DataTable({
            "paging": false,
            "lengthChange": false,
            "searching": false,
            "ordering": true,
            "info": false,
            "autoWidth": false
        });

        //copiar enlace al ticket al portapapeles
        $('#link_to_cb').click(function(){
            var link = $('#ticket_link').attr("href");
            console.log(link);
            var aux = document.createElement("input");

            // Asigna el contenido del elemento especificado al valor del campo
            aux.setAttribute("value", link);

            // Añade el campo a la página
            document.body.appendChild(aux);

            // Selecciona el contenido del campo
            aux.select();

            // Copia el texto seleccionado
            document.execCommand("copy");

            // Elimina el campo de la página
            document.body.removeChild(aux);
        });
    });
});
