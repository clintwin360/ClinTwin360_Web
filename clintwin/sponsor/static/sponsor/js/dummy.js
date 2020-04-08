





function row_template(props){
    let template = "" +
        "<tr id=\"trial-"+ props.id +"\" class=\"clickable-row\">\<" +
        "td>"+props.title+"</td>" +
        "<td>"+props.sponsor.organization+"</td>" +
        "<td>"+props.enrollmentTarget+"</td>" +
        "</tr>";
    return template;
}

$(function(){
    console.log("in this function!")
  $.getJSON("/api/trials/", function(result){
    $.each(result.results, function(i, field){
        console.log(i,field);
      $("#dummy_table").append(row_template(field));
    });
  });


    $(document).on( "click","tr.clickable-row", function() {
    console.log("clicked!!" ,$(this).attr('id'));
});

});



