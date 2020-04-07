var tableEntryTemplate = '<tr onclick=""><td><a class="sponsor-id-link" href="">';
var editButton = '<td><button class="viewbtn" type="button">View</button><button class="editbtn" type="button">Edit</button></td>';

$(function(){
  $.getJSON("/api/profile/", function(result){
    $.each(result.results, function(i, field){
      $("#sponsor-list-body").append(tableEntryTemplate +
        field.sponsor_id + '</a></td><td>' +
        field.organization + '</td><td>Date Joined: ' +
        field.date_joined + '</td><td>Notes:' +
        field.notes + '</td>' +
        editButton + '</tr>') ;
    });
  });
});
