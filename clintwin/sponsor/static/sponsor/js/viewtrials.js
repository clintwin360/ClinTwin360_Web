var tableEntryTemplate = '<td><a class="trial-id-link" href="/sponsor/trial/';
var tableRowTemplate = '<tr class="trial-element" id=trial_';
var editButton = '<td><button class="viewbtn" type="button">View</button><button class="editbtn" type="button">Edit</button></td>';


$(function(){
  $.getJSON("/api/trials/", function(result){
    $.each(result.results, function(i, field){
      $(tableRowTemplate + field.id.toString() + '>' +
        tableEntryTemplate + field.id.toString() + '">' +
        field.custom_id + '</a></td><td>' +
        field.title + '</td><td>' +
        field.status + '</td><td>' +
        field.current_recruitment + '</td><td>' +
        field.enrollmentTarget + '</td><td>Started: ' +
        field.recruitmentStartDate + '</td><td>' +
        field.recruitmentEndDate + '</td>' +
        editButton + '</tr>').appendTo('#trial-list-body') ;
    });
  });
});
