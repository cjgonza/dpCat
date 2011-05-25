

// Hacer desaparecer los mensajes tipo.

$(document).ready(function() {
    $(".cerrar").click(function () {
        $(this.parentNode).animate({ opacity: 0, height: 0 }, "slow").hide("slow");
    });

    $(".alerta-header").click(function () {
        $(this).find(".icon").toggleClass("minus").toggleClass("plus");
        $(this).parents(".alerta:first").find(".alerta-content").toggle();
    });

    $(".rechazar").click(function () {
        $(this.parentNode.parentNode).find(".form-validacion-opciones").toggle();
        $(this.parentNode.parentNode).find(".form-validacion-rechaza").toggle();
    });

    $(".videoteca-buscador-header").click(function () {
        $(this.parentNode.parentNode).find(".videoteca-buscador-content").toggle();
    });

   

    $(function() {
        var dates = $( "#from, #to" ).datepicker({
            maxDate: "+0d",
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 3,
            onSelect: function( selectedDate ) {
                var option = this.id == "from" ? "minDate" : "maxDate",
                    instance = $( this ).data( "datepicker" ),
                    date = $.datepicker.parseDate(
                        instance.settings.dateFormat ||
                        $.datepicker._defaults.dateFormat,
                        selectedDate, instance.settings );
                dates.not( this ).datepicker( "option", option, date );
           }
        });
    });




});


// Arrastra y ordena

$(function() {
    $( ".column" ).sortable({
        connectWith: ".column"
    });

    $( ".portlet" ).addClass( "ui-widget ui-widget-content ui-helper-clearfix ui-corner-all" )
        .find( ".portlet-header" )
            .addClass( "ui-widget-header ui-corner-all" )
            .prepend( "<span class='ui-icon ui-icon-minusthick'></span>")
            .end()
        .find( ".portlet-content" );

    $( ".portlet-header .ui-icon" ).click(function() {
        $( this ).toggleClass( "ui-icon-minusthick" ).toggleClass( "ui-icon-plusthick" );
        $( this ).parents( ".portlet:first" ).find( ".portlet-content" ).toggle();
    });

    $( ".portlet-header" ).disableSelection();
});
