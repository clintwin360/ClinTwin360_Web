var criteria_list = [];


function form_yes_no(props) {
    return `<form name="criteria_x" id="criteria_x" action="" method="post">` +
      `<input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">` +
      `<br><label class="criteria-response" for="criteria">${props.name} </label>` +
      `<input type="hidden" id="criteria" name="criteria" value="${props.name}"><br>` +
      `<select id="criteria-option" name="criteria-option">`+
      `<option value="${props.options[0]}" id="value">${props.options[0]}</option>`+
      `<option value="${props.options[1]}" id="value">${props.options[1]}</option>`+
      `</select>`+
      `<br><input type="checkbox" id="negated" name="negated">` +
      `<label for="negation-maker">Exclusion?</label><br>` +
        `<input type="submit" value="Add Criteria" id="add_cri">` +
        `</form><br>`
}

//add conditions to allow for multiple select
function form_select(props){
    return `<form name="criteria_x" id="criteria_x" action="" method="post">` +
      `<input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">` +
    `<br><label class="criteria-response" for="criteria" class="mdb-main-label">${props.name} </label>` +
    `<input type="hidden" id="criteria" name="criteria" value="${props.name}"><br>` +
    `<select id="criteria-option" name="criteria-option">`+
    `<option value="" disabled selected>Select values that apply</option>` +
      props.options.map(option=>`<option value="${option}">${option}</option>`) +
      `</select>`+
      `<br><input type="checkbox" id="negated" name="negated">` +
      `<label for="negation-maker">Exclusion?</label><br>` +
      `<input type="submit" value="Add Criteria" id="add_cri">` +
      `</form><br>`
}


function form_comparison(props){
      return `<form name="criteria_x" id="criteria_x" action="" method="post" novalidate>` +
      `<input type="hidden" name="csrfmiddlewaretoken" value="`+ getCookie('csrftoken') +`">` +
          `<label class="criteria-response" for="criteria">${props.name} </label>` +
          `<input type="hidden" id="criteria" name="criteria" value="${props.name}"><br>` +
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

//Document Ready
$(function(){


    //Get Searchable Criteria List
    $.getJSON("/api/criteria/?searchable=true", function(result){
          criteria_list = result.results;

          $( "#criteria-lookup" ).autocomplete({
            source: criteria_list.map(item=>item.name)
    });
    });


    //Figure out which widget form to show when lookup is submitted
    $("#criteria-lookup-form").submit(function(e) {
        e.preventDefault();
        console.log($("#criteria-lookup").val(),"form was submitted");


        let criteriaCategory = $("#criteria-lookup").val();
        let criteria_item = criteria_list.find(item=>criteriaCategory == item.name);
        console.log(criteria_item);
        let form_template = null;

        if (criteria_item.valueType == 'enter_val_comp'){
            console.log("HERE")
            form_template = form_comparison(criteria_item)
        }

        if (criteria_item.valueType == 'enter_val_fixed'){
            form_template = form_comparison(criteria_item)
        }

        if (criteria_item.valueType =='yes_no'){
            form_template = form_yes_no(criteria_item)
        }

        if (criteria_item.valueType == 'pick_one'){
            form_template = form_select(criteria_item)
        }

        if (criteria_item.valueType == 'list'){
            form_template = form_select(criteria_item)
        }

        $("#selected-criteria-form").append(form_template);


        return false;
    });

    //To use later for multiselect forms
    $('option').mousedown(function(e) {
        e.preventDefault();
        $(this).prop('selected', !$(this).prop('selected'));
        return false;
    });



    });
