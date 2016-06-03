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

    $("#marcar-todo").on('ifChecked', function() {
        $(".minimal").iCheck("check");
        mostrarGenerarTicket();
    });
    $("#marcar-todo").on('ifUnchecked', function() {
        $(".minimal").iCheck("uncheck");
        mostrarGenerarTicket();
    });

    $(".minimal").on('ifUnchecked', function() {
        mostrarGenerarTicket();
    });
    $(".minimal").on('ifChecked', function() {
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
        //inicializar paametros de datatable
        $('#table_enproceso').DataTable({
            "paging": true,
            "pageLength": 25,
            "lengthChange": false,
            "searching": true,
            "ordering": true,
            "info": true,
            "autoWidth": false,
            "language": {
                "lengthMenu": "Mostrar _MENU_ resultados",
                "emptyTable": "No hay resultados que mostrar",
                "info": "Página _PAGE_ de _PAGES_",
                "infoEmpty":  "Página _PAGE_ de _PAGES_",
                "search":     "Buscar:",
                "zeroRecords":    "No hay resultados que concuerden con la búsqueda",
                "infoFiltered":   "",
                "paginate": {
                    "first":      "Primero",
                    "last":       "Último",
                    "next":       "Siguiente",
                    "previous":   "Anterior"
                },
            },
            "columns": [
               { "orderDataType": "dom-checkbox" },
               null,
               { "type": 'date-eu', "targets": 0 },
               null,
               null,
               null,
               null
             ]
        });
        //inicializar paametros de datatable
        $('#table_videoteca').DataTable({
            "paging": true,
            "pageLength": 25,
            "lengthChange": false,
            "searching": true,
            "ordering": true,
            "info": true,
            "autoWidth": false,
            "language": {
                "lengthMenu": "   Mostrar _MENU_ resultados",
                "emptyTable":     "No hay resultados que mostrar",
                "infoEmpty":      "Página _PAGE_ de _PAGES_",
                "info":           "Página _PAGE_ de _PAGES_",
                "search":         "Buscar:",
                "zeroRecords":    "No hay resultados que concuerden con la búsqueda",
                "infoFiltered":   "",
                "paginate": {
                    "first":      "Primero",
                    "last":       "Último",
                    "next":       "Siguiente",
                    "previous":   "Anterior"
                },
            },
            "columns": [
               null,
               { "type": 'date-eu', "targets": 0 },
               null,
               null,
               null
             ]
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
