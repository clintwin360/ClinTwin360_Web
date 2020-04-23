function request_row(props){
    let template = "" +
        "<tr id=\"request-"+ props.id +"\" class=\"clickable-row request-element\">" +
        "<td>"+props.sponsor.organization+"</td>" +
        "<td>"+props.criterion_req+"</td>" +
        "<td>"+props.values+"</td>" +
        "<td>"+props.notes+"</td>" +
        "<td><a class=\"btn btn-info editbtn\" href=\"/sponsor/criteriarequest/"+props.id+"\">View</td>" +
        "</tr>";
    return template;
}

$(function(){
  $.getJSON("/api/sponsor_request/", function(result){
    $.each(result.results, function(i, field){
     $("#request-list-body").append(request_row(field));
    });
  });
});


/*

"<td><a class=\"btn btn-danger deletebtn\" href=\"/sponsor/deleteprofile/"+props.id+"\">Delete</td>" +
*/
