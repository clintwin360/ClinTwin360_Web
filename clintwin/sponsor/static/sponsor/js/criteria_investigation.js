function formElement(props){
      return `<br><label class="criteria-response" id="comparison-${props.index}" for="comparison-${props.index}">${props.title} </label>` +
          `<select id="comparison-selected" name="comparison">`+
                 `<option value="gte">Greater than or equal to</option>`+
                 `<option value="lte">Less than or equal to</option>`+
                 `<option value="e">Equals</option>`+
                 `<option value="nte">Does not Equal</option>`+
            `</select>`+
          `<input type="text" id="criteria-response-${props.index}" name="criteria-response-${props.index}"><br><br>` +
          `<input type="submit" value="Add Criteria" id="add_cri"><br>`
}

function formElement_text(props, criteria_values){
  var count = criteria_values.length;
  var criteria_x = props.title;
  var i = 0;
  // console.log(props.title, "IS IT!"); //DEBUG--
  // console.log(criteria_values, "used"); //DEBUG--

  //Selector for Yes/No
  if (count == 2 && (criteria_values[0] == "Yes" || criteria_values[0] == "No")) {
    return `<br><label class="criteria-response" id="comparison-${props.index}" for="comparison-${props.index}">${props.title} </label>` +
      `<select id="comparison-${props.index}" name="comparison">`+
      `<option value="0" id="criteria-response-${props.index}">`+ criteria_values[0]+ `</option>`+
      `<option value="1" id="criteria-response-${props.index}">`+ criteria_values[1]+ `</option>`+
      `</select>`+
      `<br><input type="submit" value="Add Criteria" id="add_cri"><br>`
  }
  //Selector for multiple selects
  else {
    var start = `<option>`;
    for(var i = 0; i < criteria_values.length; i++) {
        var el = criteria_values[i] ;
        // console.log(el);
        start = start + el;
        if(i<criteria_values.length-1){
          start = start + `</option><option>`;
        } else {
          start = start + `</option>`;
        }
        // console.log(start);
  }
    return `<br><label class="criteria-response" id="comparison-${props.index}" for="comparison-${props.index}" class="mdb-main-label">${props.title} </label>` +
    `<select class="mdb-select md-form colorful-select dropdown-danger" multiple id="comparison-${props.index}" name="comparison" size="` + count +`">`+
    `<option value="" disabled selected>Select values that apply</option>` +
      start +
      `</select>`+
      `<br><input type="checkbox" id="negation-maker" name="negated">` +
      `<label for="negation-maker"> Does not have</label><br>` +
      `<br><input type="submit" value="Add Criteria" id="add_cri"><br>`

}
}


// Function to split criteria values
function parse_criteria_vals(vals){
  // Remove "["" and ""]" from front & back of vals text
  var x = vals.substring(1, vals.length - 1);
  // console.log(x); //DEBUG--
  //Replace all qotation marks with nothing
  var y = x.replace(/['"]+/g, '');
  // console.log(y); //DEBUG--
  //Replace any amount of whitespace before or after a `,` to nothing & split to array
  var vals_array = y.replace(/\s*,\s*/ig, ',').split(',');
  // console.log(vals_array); //DEBUG--
  return vals_array;
}

// Function to  grab the criteria values
function get_criteria_options(props){
  console.log(props.title); //DEBUG--
  var criteria_values = [];
  var criteria = props.title;
  var currentPage = 0;
     $.getJSON("/api/criteria/", function(result){
          var pages = Math.ceil(result.count / 10);
          // console.log(result.count, "is result.count") //DEBUG --
          console.log(pages); //DEBUG --
          while (currentPage < pages){
            currentPage++;
            // console.log(currentPage, "current page");
            $.getJSON("/api/criteria/?page="+currentPage, function(result){
                $.each(result.results, function(i, field){
                  // if (field.searchable){
                    var criteria_sel = field.name;
                    // console.log(criteria_sel, "is the selected criteria being matched")
                    if (field.searchable && (criteria_sel.localeCompare(criteria) == 0)) {

                      // console.log(criteria_sel, "matches ", criteria); //DEBUG--
                      // console.log(field.options); //DEBUG--
                      // Parse criteria values into list
                      criteria_values = parse_criteria_vals(field.options);
                      // console.log(criteria_values, "is criteria_values");
                      return $("#selected-criteria-form").append(formElement_text(props, criteria_values))
                      // console.log(criteria_values[0], "is the first criteria_value");//DEBUG--
                    }
                });
              });
          }
    });
}


$(function(){
  $("#criteria-lookup-form").submit(function(e) {
      console.log($("#criteria-lookup").val(),"form was submitted");

      let criteriaCount = 0;
      let criteriaCategory = $("#criteria-lookup").val();
      // For age, weight, height, or BMI show selector
      if ((criteriaCategory.localeCompare("age") == 0) || (criteriaCategory.localeCompare("height") == 0) ||
      (criteriaCategory.localeCompare("weight") == 0) || (criteriaCategory.localeCompare("BMI") == 0)) {
        $("#selected-criteria-form").append(formElement({'title':criteriaCategory,'index':criteriaCount}))
        e.preventDefault();
        criteriaCount++;
      } // Other criteria get selecor shwoing values from criteria value list
      else {
        get_criteria_options({'title':criteriaCategory,'index':criteriaCount})
        e.preventDefault();
        criteriaCount++;
      }

  });

});
