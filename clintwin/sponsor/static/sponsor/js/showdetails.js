function trial_details(id){
    let windowTemplate = "" + "<div id=\"pane\">" +
        "<object type=\"text/html\" data=\"/sponsor/pane/"+id+
        "\" id=\"trial-detail-pane\" class=\"trial-detail-pane\" width=\"900px\" height=\"600px\" style=\"overflow:auto;\">" +
        "</object></div>"
    return windowTemplate;
};

$(document).on( "click","tr.clickable-row", function() {
    if (document.getElementById('pane')){
        document.getElementById('pane').parentNode.removeChild(document.getElementById('pane'));
    }
    var idArray = this.id.toString().split("-");
    var trialId = idArray[1];
    $("#trial-details").append(trial_details(trialId));

});
