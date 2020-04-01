var cardtitleTemplate = '<h5 class="card-title">';
var cardtextTemplate = '<p class="card-text">';
var cardtextsmallTemplate = '<p class="card-text"><small class="text-muted">'
var cardTemplate = '<div class="card">';
var cardbodyTemplate = '<div class="card-body">';

$(function(){
  $.getJSON("/sponsor/trial/?id=12345", function(result){
    $.each(result.results, function(i, field){
      $("#cardlist").append(cardTemplate + cardbodyTemplate + cardtitleTemplate + field.title + '</h5>' + cardtextTemplate + field.description + "</p>" + cardtextsmallTemplate + 'Recruitment Start: ' + field.recruitmentStartDate + " Recruitment End: " + field.recruitmentEndDate + ' Enrollment Target: ' + field.enrollmentTarget + '</small></p></div></div>');
    });
  });
});
