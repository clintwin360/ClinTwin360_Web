var cardtitleTemplate = '<h5 class="card-title">';
var cardtextTemplate = '<p class="card-text">';
var cardtextsmallTemplate = '<p class="card-text"><small class="text-muted">'
var cardTemplate = '<div class="card">';
var cardbodyTemplate = '<div class="card-body bg-light flex-row justify-content-between align-items-cent">';
var radiocardTemplate = '<label class="mt-3"><input type="radio" name="trialselect" class="card-input-element d-none" id="test">';

$(function(){
  $.getJSON("/sponsor/trial/?id=12345", function(result){
    $.each(result.results, function(i, field){
      $("#cardlist").append(radiocardTemplate + cardTemplate + cardbodyTemplate + cardtitleTemplate + field.title + '</h5>' + cardtextTemplate + field.description + "</p>" + cardtextsmallTemplate + 'Recruitment Start: ' + field.recruitmentStartDate + "<br>Recruitment End: " + field.recruitmentEndDate + '<br>Enrollment Target: ' + field.enrollmentTarget + '</small></p></div></div></label<br>');
    });
  });
});
