function trial_row(props){
    let percentage = props.current_recruitment / props.enrollmentTarget;
    let numColor = "black";
    console.log(percentage);
    if (percentage <= .34){
        numColor = "red";
    }
    else if (percentage > .35 && percentage < .70){
        numColor = "orange";
    }
    else {
        numColor = "green";
    }
    let template = "" +
        "<tr id=\"trial-"+ props.id +"\" class=\"clickable-row trial-element\">" +
        "<td><a class=\"trial-id-link\" href=\"/sponsor/trial/"+ props.id + "\">" + props.custom_id + "</a></td>" +
        //"<td>"+props.title+"</td>" +
        "<td>"+props.status+"</td>" +
        "<td>"+(props.current_recruitment.toString().fontcolor(numColor))+" / "+props.enrollmentTarget+"</td>" +
        "<td>"+props.recruitmentStartDate+"</td>" +
        "<td>"+props.recruitmentEndDate+"</td>" +
        "</tr>";
    return template;
}

$(function(){
    console.log("sponsor_id",sponsor_id);


  $.getJSON("/api/trials/?sponsor_id=" + sponsor_id, function(result){
    $.each(result.results, function(i, field){
     $("#trial-list-body").append(trial_row(field));
    });
  });
});

/*
"<td><a class=\"btn btn-info editbtn\" href=\"/sponsor/updatetrial/"+props.id+"\">Edit</td>" +
"<td><a class=\"btn btn-danger deletebtn\" href=\"/sponsor/deletetrial/"+props.id+"\">Delete</td>"
*/
