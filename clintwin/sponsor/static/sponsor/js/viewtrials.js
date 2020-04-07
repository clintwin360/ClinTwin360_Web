var tableEntryTemplate = '<td><a class="sponsor-id-link" href="/api/trial/?id="';
var tableRowTemplate = '<tr onclick="" id="';
var editButton = '<td><button class="viewbtn" type="button">View</button><button class="editbtn" type="button">Edit</button></td>';


$(function(){
  $.getJSON("/api/trials/", function(result){
    $.each(result.results, function(i, field){
      $("#trial-list-body").append(tableRowTemplate + field.id + '">' +
        tableEntryTemplate + field.id + '">' +
        field.custom_id + '</a></td><td>' +
        field.title + '</td><td>' +
        field.status + '</td><td>' +
        field.current_recruitment + '</td><td>' +
        field.enrollmentTarget + '</td><td>Started: ' +
        field.recruitmentStartDate + '</td><td>' +
        field.recruitmentEndDate + '</td>' +
        editButton + '</tr>') ;
    });
  });
});
