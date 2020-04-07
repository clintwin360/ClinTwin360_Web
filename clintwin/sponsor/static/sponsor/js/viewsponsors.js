var tableEntryTemplate = '<td><a class="sponsor-id-link" href="/sponsor/profile/';
var tableRowTemplate = '<tr onclick="" id=sponsor_';
var editButton = '<td><button class="viewbtn" type="button">View</button><button class="editbtn" type="button">Edit</button></td>';

$(function(){
  $.getJSON("/api/profile/", function(result){
    $.each(result.results, function(i, field){
      $("#sponsor-list-body").append(tableRowTemplate + field.id.toString() + '>' +
        tableEntryTemplate + field.id.toString() + '">' +
        field.id + '</a></td><td>' +
        field.organization + '</td><td>Date Joined: ' +
        field.date_joined + '</td><td>Notes:' +
        field.notes + '</td>' +
        editButton + '</tr>') ;
    });
  });
});
