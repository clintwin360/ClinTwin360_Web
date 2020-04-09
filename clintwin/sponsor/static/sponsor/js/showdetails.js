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
    let template = "" + "<div>" +
        "<object type=\"text/html\" data=\"/sponsor/trial/"+id+
        "\"width=\"800px\" height=\"600px\" style=\"overflow:auto;border:5px ridge blue\" class=\"trial-detail-page\">" +
        "</object></div>"
    return template;
};

$(document).on( "click","tr.clickable-row", function() {
    var idArray = this.id.toString().split("-");
    var trialId = idArray[1];
    $("#trial-details").removeClass("trial-detail-page").append(trial_details(trialId));
});
