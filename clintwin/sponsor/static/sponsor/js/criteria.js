var criteria_list = [];


function form_yes_no(props) {
    return `<form name="add-criteria" id="add-criteria" data-criteria="${props.id}" action="">` +
      `<input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">` +
      `<br><label class="criteria-response" for="criteria">${props.name} </label>` +
      `<input type="hidden" id="criteria" name="criteria" value="${props.name}"><br>` +
      `<select id="criteria-value" name="criteria-value">`+
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
    let select_type = '';
    let option_class = '';
    if (props.valueType === 'list') {
        select_type = 'Multiple';
        option_class = 'multi-option'
    }

    return `<form name="add-criteria" id="add-criteria" data-criteria="${props.id}"  action="" method="post">` +
      `<input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">` +
    `<br><label class="criteria-response" for="criteria" class="mdb-main-label">${props.name} </label>` +
    `<input type="hidden" id="criteria" name="criteria" value="${props.name}"><br>` +
    `<select ${select_type} id="criteria-value" name="criteria-value">`+
    `<option value="" disabled selected>Select values that apply</option>` +
      props.options.map(option=>`<option class="${option_class}" value="${option}">${option}</option>`) +
      `</select>`+
      `<br><input type="checkbox" id="negated" name="negated">` +
      `<label for="negation-maker">Exclusion?</label><br>` +
      `<input type="submit" value="Add Criteria" id="add_cri">` +
      `</form><br>`
}


function form_comparison(props){
      return `<form name="add-criteria" id="add-criteria" data-criteria="${props.id}"  action="" method="post" novalidate>` +
      `<input type="hidden" name="csrfmiddlewaretoken" value="`+ getCookie('csrftoken') +`">` +
          `<label class="criteria-response" for="criteria">${props.name} </label>` +
          `<input type="hidden" id="criteria" name="criteria" value="${props.name}"><br>` +
          `<select id="comparison" name="comparison">`+
                 `<option value="gte">Greater than or equal to</option>`+
                 `<option value="lte>Less than or equal to</option>`+
                 `<option value="equals">Equals</option>`+
                 `<option value="ne">Does not Equal</option>`+
            `</select>`+
          `<input type="text" id="criteria-value" name="criteria-value"><br>` +
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


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

//Document Ready
$(function(){

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });

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
        $("#selected-criteria-form").empty();

        let criteriaCategory = $("#criteria-lookup").val();
        let criteria_item = criteria_list.find(item=>criteriaCategory === item.name);
        let form_template = null;

        if (criteria_item.valueType === 'enter_val_comp'){
            form_template = form_comparison(criteria_item)
        }

        if (criteria_item.valueType === 'enter_val_fixed'){
            form_template = form_comparison(criteria_item)
        }

        if (criteria_item.valueType ==='yes_no'){
            form_template = form_yes_no(criteria_item)
        }

        if (criteria_item.valueType === 'pick_one'){
            form_template = form_select(criteria_item)
        }

        if (criteria_item.valueType === 'list'){
            form_template = form_select(criteria_item)
        }

        $("#selected-criteria-form").append(form_template);


        return false;
    });


    //Editing a Criteria
    $(document).on( "click",".edit-criteria", function(e) {
        e.preventDefault();
        console.log($(this).parent());
    });


    //Submitting a Criteria
    $(document).on( "submit","#add-criteria", function(e) {
        e.preventDefault();
        let trial_id = $( "#criteria-lookup-form" ).data('trial');
        let criteria_id = $(this).data('criteria');

        let serialized_data = $(this).serializeArray();

        let criteria_value = serialized_data.filter(item=>item.name==='criteria-value')

        if (criteria_value.length > 1){
            criteria_value = criteria_value.map(item=>item.value);
            criteria_value = criteria_value.toString()
        }else{
            criteria_value = criteria_value[0].value
        }

        let criteria_comparison = 'equals';
        if (serialized_data.includes(item=>item.name==='comparison')){
            let comparison = serialized_data.find(item=>item.name==='comparison');
            criteria_comparison = comparison.value;
        }


        let criteria_data = {
            "value": criteria_value,
            "comparison": criteria_comparison,
            "criteriaType": "inclusion",
            "negated": false,
            "criteria": criteria_id,
            "trial": trial_id
        };

        console.log(criteria_data);

        $.ajax({
            type: "POST",
            url: "/api/criteria_response/",
            data: JSON.stringify(criteria_data),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data){
                location.reload();
            },
            failure: function(errMsg) {
                console.error(errMsg);
            }
        });
        return false
    });




    $(document).on( "click",".delete-criteria", function(e) {
        e.preventDefault();
        let id = $(this).data('id');
        let row = $(this).parent().parent();
        //Delete

        $.ajax({
            url: `/api/criteria_response/${id}`,
            type: 'DELETE',
            success: function(result) {
                //Remove Row
                console.log("success!",result);
                row.remove();
            }
        });
    });





});
