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
    });
});
