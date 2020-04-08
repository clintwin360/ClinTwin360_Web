/*function clickTrial() {
    console.log(this);
    var idArray = this.id.toString().split("_");
    var trialId = idArray[1];
    $.getJSON("/api/trial/?id=" + trialId, function(result){
        $('#trial-details').append('<p>The trial selected has a pk of ' + trialId + '</p><br>');
    });
};

        /*

        });
    });
*/

$(document).on( "click","tr.clickable-row", function() {
    var idArray = this.id.toString().split("-");
    var trialId = idArray[1];
    $.getJSON("/api/trials/?id=" + trialId, function(result){
        $('#trial-details').append('<p>The trial selected has a pk of ' + trialId + '</p><br>');
    });
});
