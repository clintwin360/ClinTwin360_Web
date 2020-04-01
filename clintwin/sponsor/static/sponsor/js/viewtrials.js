$(function(){
  $.getJSON("/sponsor/trial/", function(result){
    $.each(result.results, function(i, field){
      $(document.getElementById("tabledata")).append("<td>" + field.trialId + "</td>").append("<td>" + field.title + "</td>").append("<td>" + field.objective + "</td>").append("<td>" + field.description + "</td>").append("<td>" + field.recruitmentStartDate + "</td>").append("<td>" + field.recruitmentEndDate + "</td>").append("<td>" + field.enrollmentTarget + "</td>");
    });
  });
});
