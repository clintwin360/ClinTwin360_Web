$(function(){
    $(".radio input[type='radio']").on( 'click', function(){
    if ($("#fake").is(":checked")) {
         $("#trialdetails").append('<p>Super fake details</p>');
    } else if ($("#fake").is(":checked")) {
         $("#trialdetails").append('<p>Presumably more real details</p>');
    }
    });
});
