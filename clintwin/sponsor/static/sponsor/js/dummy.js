





function textTemplate(props){
    var template = "<div>" + props.text + "</div>";
    return template;
}

$(function(){
  $.getJSON("/sponsor/questions/", function(result){
    $.each(result.results, function(i, field){
      $("div").append("<div>" + field.text + "</div>");
    });
  });
});