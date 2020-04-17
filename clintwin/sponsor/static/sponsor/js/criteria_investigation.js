
function formElement(props){
    return `<label class="criteria-response" for="comparison-">${props.title}</label>` +
        `<select id="comparison-${props.index}" name="comparison">`+
               `<option value="gte">Greater than or equal to</option>`+
               `<option value="lte">Less than or equal to</option>`+
               `<option value="e">Equals</option>`+
               `<option value="nte">Does not Equal</option>`+
          `</select>`+
        `<input type="text" id="criteria-response-${props.index}" name="criteria-response-${props.index}"><br><br>`
}



$(function(){

$("#criteria-lookup-form").submit(function(e) {
    console.log($("#criteria-lookup").val(),"form was submitted");
    let criteriaCount = $( "criteria-response" ).length;
    let criteriaCategory = $("#criteria-lookup").val();
    $("#selected-criteria-form").append(formElement({'title':criteriaCategory,'index':criteriaCount}))
    e.preventDefault();
});





});



