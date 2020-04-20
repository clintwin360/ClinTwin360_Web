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
  $.getJSON("/api/trials/", function(result){
    $.each(result.results, function(i, field){
    });
  });

      $( ".card" ).hover(
  function() {
    $(this).addClass('mask red').css('cursor', 'pointer');
  }, function() {
    $(this).removeClass('mask red');
  }
);
    $(document).on( "click","tr.clickable-row", function() {
    console.log("clicked!!" ,$(this).attr('id'));
});

});



