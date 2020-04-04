var tableEntryTemplate = '<tr onclick=""><div id="tabledata"><td><a class="sponsor-id-link" href="">';

$(function(){
  $.getJSON("/sponsor/sponsors/", function(result){
    $.each(result.results, function(i, field){
      $("#sponsor-list-body").append(tableEntryTemplate + field.sponsor_id + '</a></td><td>' + field.organization + '</td><td>Starterd: ' + field.date_joined + '</td><td>' + field.notes + '</td></div></tr>');
    });
  });
});
