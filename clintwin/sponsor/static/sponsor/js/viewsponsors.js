var tableEntryTemplate = '<td><a class="sponsor-id-link" href="/sponsor/profile/';
var tableRowTemplate = '<tr onclick="" id=sponsor_';
var editButtonOld = '<td><button class="viewbtn" type="button">View</button><button class="editbtn" type="button">Edit</button></td>';
var editButton = '<td><a class="btn btn-info editbtn" href="/sponsor/updateprofile/';
var deleteButton = '<a class="btn btn-danger deletebtn" href="/sponsor/deleteprofile/';

$(function(){
  $.getJSON("/api/profile/", function(result){
    $.each(result.results, function(i, field){
      $("#sponsor-list-body").append(tableRowTemplate + field.id.toString() + '>' +
        tableEntryTemplate + field.id.toString() + '">' +
        field.id + '</a></td><td>' +
        field.organization + '</td><td>' +
        field.date_joined + '</td><td>' +
        field.notes + '</td>' +
        editButton + field.id.toString() + '">Edit</a>' +
        deleteButton + field.id.toString() + '">Delete</a></td></tr>').appendTo('#trial-list-body') ;
    });
  });
});
