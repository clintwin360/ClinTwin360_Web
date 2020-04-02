var radiocardTemplate = '<label><input type="radio" name="trialselect" class="card-input-element d-none" id="test">';
var cardTemplate = '<div class="card">';
var cardheaderTemplate = '<div class="card-header"><h5 class="card-title">';
var cardbodyTemplate = '<div class="card-body bg-light flex-row justify-content-between align-items-cent">';
var cardtitleTemplate = '<h6 class="card-text">';
var cardtextTemplate = '<p class="card-text">';
var cardtextsmallTemplate = '<p class="card-text"><small class="text-muted">'

$(function(){
  $.getJSON("/sponsor/trial/?id=12345", function(result){
    $.each(result.results, function(i, field){
      $("#cardlist").append(radiocardTemplate + cardTemplate + cardheaderTemplate + field.title + '</h5><small>0/' + field.enrollmentTarget + '</small></div>' + cardbodyTemplate + cardtextTemplate + field.description + "</p>" + cardtextsmallTemplate + 'Recruitment Period: ' + field.recruitmentStartDate + " to " + field.recruitmentEndDate + '</small></p></div></div></label>');
    });
  });
});
