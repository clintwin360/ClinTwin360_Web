$(document).ready(function(){
    $(document).on('click', 'input[type=radio]', function(){
        var value = $("#trialselect").val();
        if (value == 'fake') {
             $("#trialdetails").append('<p>Super fake details</p>');
        } else if (value == 'test') {
             $("#trialdetails").append('<p>Presumably more real details</p>');
        }
    });
});
