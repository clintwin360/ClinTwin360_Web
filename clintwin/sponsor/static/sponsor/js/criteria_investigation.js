function formElement(props){
      return `<form name="criteria_x" id="criteria_x" action="" method="post" novalidate>` +
      `<input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">` +
          `<label class="criteria-response" for="comparison-${props.index}">${props.title} </label>` +
          `<input type="hidden" id="criteria" name="criteria" value="${props.title}"><br>` +
          `<select id="comparison" name="comparison">`+
                 `<option value="gte">Greater than or equal to</option>`+
                 `<option value="lte>Less than or equal to</option>`+
                 `<option value="equals">Equals</option>`+
                 `<option value="ne">Does not Equal</option>`+
            `</select>`+
          `<input type="text" id="value" name="value"><br>` +
          `<br><input type="checkbox" id="negated" name="negated">` +
          `<label for="negation-maker">Exclusion?</label><br>` +
          `<input type="submit" value="Add Criteria" id="add_cri">` +
          `</form><br>`
}





function formElement_text(props, criteria_values){
  var count = criteria_values.length;
  var criteria_x = props.title;
  var i = 0;
  var val_1 = criteria_values[0];
  var val_2 = criteria_values[1];
  // console.log(props.title, "IS IT!"); //DEBUG--
  // console.log(criteria_values, "used"); //DEBUG--

  //Selector for Yes/No
  if (count == 2 && (criteria_values[0] == "Yes" || criteria_values[0] == "No")) {
    return `<form name="criteria_x" id="criteria_x" action="" method="post">` +
      `<input type="hidden" name="csrfmiddlewaretoken" value="`+ getCookie('csrftoken') +`">` +
      `<br><label class="criteria-response" for="comparison-${props.index}">${props.title} </label>` +
      `<input type="hidden" id="criteria" name="criteria" value="${props.title}"><br>` +
      `<select id="value" name="value">`+
      `<option value="` + val_1 + `" id="value">`+ criteria_values[0]+ `</option>`+
      `<option value="` + val_2 + `" id="value">`+ criteria_values[1]+ `</option>`+
      `</select>`+
      `<br><input type="checkbox" id="negated" name="negated">` +
      `<label for="negation-maker">Exclusion?</label><br>` +
        `<input type="submit" value="Add Criteria" id="add_cri">` +
        `</form><br>`
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
    return `<form name="criteria_x" id="criteria_x" action="" method="post">` +
      `<input type="hidden" name="csrfmiddlewaretoken" value="`+ getCookie('csrftoken') +`">` +
    `<br><label class="criteria-response" id="criteria" for="comparison-${props.index}" class="mdb-main-label">${props.title} </label>` +
    `<input type="hidden" id="criteria" name="criteria" value="${props.title}"><br>` +
    `<select class="mdb-select md-form colorful-select dropdown-danger" multiple id="value" name="value" size="` + count +`">`+
    `<option value="" disabled selected>Select values that apply</option>` +
      start +
      `</select>`+
      `<br><input type="checkbox" id="negated" name="negated">` +
      `<label for="negation-maker">Exclusion?</label><br>` +
      `<input type="submit" value="Add Criteria" id="add_cri">` +
      `</form><br>`

}
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


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
      } // Other criteria get selecor shwoing values from criteria value list
      else {
        get_criteria_options({'title':criteriaCategory,'index':criteriaCount})
        e.preventDefault();
      }

  });

});
