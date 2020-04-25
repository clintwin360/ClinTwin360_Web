function sponsor_row(props){
    let template = "" +
        "<tr id=\"sponsor-"+ props.id +"\" class=\"clickable-row sponsor-element\">" +
        "<td><a class=\"sponsor-id-link\" href=\"/sponsor/profile/"+ props.id + "\">" + props.id + "</a></td>" +
        "<td>"+props.organization+"</td>" +
        "<td>"+props.contactPerson+" : <a href=\"mailto:"+props.email+"\">"+props.email+"</a></td>" +
        "<td>"+props.date_joined+"</td>" +
        "<td>"+props.notes+"</td>" +
        "<td><a class=\"btn btn-info editbtn\" href=\"/sponsor/updateprofile/"+props.id+"\">Edit</td>" +
        "<td><a class=\"btn btn-danger deletebtn\" href=\"/sponsor/deleteprofile/"+props.id+"\">Delete</td>" +
        "</tr>";
    return template;
}

$(function(){
  $.getJSON("/api/profile/", function(result){
    $.each(result.results, function(i, field){
      console.log(field);
     $("#sponsor-list-body").append(sponsor_row(field));
    });
  });
});
