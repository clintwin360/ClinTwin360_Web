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



function trial_details(id){
    let template = "" + "<div id=\"pane\">" +
        "<object type=\"text/html\" data=\"/sponsor/pane/"+id+
        "\" id=\"trial-detail-pane\" class=\"trial-detail-pane\">" +
        "</object></div>"
    return template;
};

$(document).on( "click","tr.clickable-row", function() {
    if (document.getElementById('pane')){
        document.getElementById('pane').parentNode.removeChild(document.getElementById('pane'));
    }
    var idArray = this.id.toString().split("-");
    var trialId = idArray[1];
    $("#trial-details").append(trial_details(trialId));

});
