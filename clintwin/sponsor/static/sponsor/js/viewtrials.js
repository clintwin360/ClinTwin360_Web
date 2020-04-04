var tableEntryTemplate = '<tr onclick=""><div id="tabledata"><td><a class="trial-id-link" href="">';
var cardTemplate = '<div class="card">';
var cardheaderTemplate = '<div class="card-header"><h5 class="card-title">';
var cardbodyTemplate = '<div class="card-body bg-light flex-row justify-content-between align-items-cent">';
var cardtitleTemplate = '<h6 class="card-text">';
var cardtextTemplate = '<p class="card-text">';
var cardtextsmallTemplate = '<p class="card-text"><small class="text-muted">';

$(function(){
  $.getJSON("/sponsor/trials/", function(result){
    $.each(result.results, function(i, field){
      $("#trial-list-body").append(tableEntryTemplate + field.trialId + '</a></td><td>' + field.title + '</td><td>Starterd: ' + field.recruitmentStartDate + '</td><td>' + field.enrollmentTarget + '</td><td>' + field.recruitmentEndDate + '</td></div></tr>');
    });
  });
});
