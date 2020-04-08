function trial_row(props){
    let template = "" +
        "<tr id=\"trial-"+ props.id +"\" class=\"clickable-row trial-element\">" +
        "<td><a class=\"trial-id-link\" href=\"/sponsor/trial/"+ props.id + "\">" + props.custom_id + "</a></td>" +
        "<td>"+props.title+"</td>" +
        "<td>"+props.status+"</td>" +
        "<td>"+props.current_recruitment+"</td>" +
        "<td>"+props.enrollmentStartDate+"</td>" +
        "<td>"+props.recruitmentStartDate+"</td>" +
        "<td>"+props.recruitmentEndDate+"</td>" +
        "<td><a class=\"btn btn-info editbtn\" href=\"/sponsor/updatetrial/"+props.id+"\">Edit</td>" +
        "<td><a class=\"btn btn-danger deletebtn\" href=\"/sponsor/deletetrial/"+props.id+"\">Delete</td>" +
        "</tr>";
    return template;
}

$(function(){
  $.getJSON("/api/trials/", function(result){
    $.each(result.results, function(i, field){
     $("#trial-list-body").append(trial_row(field));
    });
  });
});
