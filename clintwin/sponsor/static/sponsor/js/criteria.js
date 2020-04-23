var criteria_list = [];


function selected_option(option_value,default_value){
    if (Array.isArray(default_value)){
        if (default_value.includes(option_value)){
            return `selected`
        } else{
            return ``
        }
    } else{
        if (option_value === default_value){
            return `selected`
        } else{
            return ``
        }
    }
}

function form_yes_no(props,defaults) {
    console.log(defaults);
    let default_comparison = null;
    let default_value = '';
    let submit_text = 'Add Criteria'
    let method = "post";
    let id = "add-criteria";
    let data_id = "";
    if (defaults){
        default_comparison = defaults.comparison;
        default_value = defaults.value;
        submit_text = 'Update';
        method = "put";
        id = "edit-criteria";
        data_id = `data-id="${defaults.id}"`
    }

    return `<form name="${id}" id="${id}" data-criteria="${props.id}" ${data_id} action="" method="${method}">` +
      `<br><label class="criteria-response" for="criteria">${props.name} </label>` +
      `<input type="hidden" id="criteria" name="criteria" value="${props.name}"><br>` +
      `<select id="criteria-value" name="criteria-value">`+
      `<option value="Yes" id="value" ${selected_option("Yes",default_value)}>Yes</option>`+
      `<option value="No" id="value" ${selected_option("No",default_value)}>No</option>`+
      `</select>`+
      `<br><input type="checkbox" id="negated" name="negated">` +
      `<label for="negation-maker">Exclusion?</label><br>` +
        `<button type="button" value="Cancel" id="cancel-criteria">Cancel</button>` +
        `<input type="submit" value="${submit_text}" id="add_cri">` +
        `</form><br>`
}

//add conditions to allow for multiple select
function form_select(props,defaults){
    let select_type = '';
    let option_class = '';
    if (props.valueType === 'list') {
        select_type = 'Multiple';
        option_class = 'multi-option'
    }

    let default_comparison = null;
    let default_value = '';
    let submit_text = 'Add Criteria';
    let method = "post";
    let id = "add-criteria";
    let data_id = "";
    if (defaults){
        default_comparison = defaults.comparison;
        default_value = defaults.value;
        submit_text = 'Update';
        method = "put";
        id = "edit-criteria";
        data_id = `data-id="${defaults.id}"`
    }

    return `<form name="${id}" id="${id}" data-criteria="${props.id}" ${data_id} action="" method="${method}">` +
    `<br><label class="criteria-response" for="criteria" class="mdb-main-label">${props.name} </label>` +
    `<input type="hidden" id="criteria" name="criteria" value="${props.name}"><br>` +
    `<select ${select_type} id="criteria-value" name="criteria-value">`+
    `<option value="" disabled selected>Select values that apply</option>` +
     props.options.map(option=>`<option class="${option_class}" value="${option}" ${selected_option(option,default_value)}>${option}</option>`) +
    `</select>`+
    `<br><input type="checkbox" id="negated" name="negated">` +
    `<label for="negation-maker">Exclusion?</label><br>` +
    `<button type="button" value="Cancel" id="cancel-criteria">Cancel</button>` +
    `<button type="submit" value="${submit_text}" id="add_cri">${submit_text}</button>` +
    `</form><br>`
}


function form_comparison(props,defaults){
    let default_comparison = null;
    let default_value = '';
    let submit_text = 'Add Criteria'
    let method = "post";
    let id = "add-criteria";
    let data_id = "";
    if (defaults){
        default_comparison = defaults.comparison;
        default_value = defaults.value;
        submit_text = 'Update';
        method = "put";
        id = "edit-criteria";
        data_id = `data-id="${defaults.id}"`
    }

      return `<form name="${id}" id="${id}" data-criteria="${props.id}" ${data_id} action="" method="${method}" novalidate>` +
          `<label class="criteria-response" for="criteria">${props.name} </label>` +
          `<input type="hidden" id="criteria" name="criteria" value="${props.name}"><br>` +
          `<select id="comparison" name="comparison">`+
                 `<option value="gte" ${selected_option("gte",default_comparison)}>Greater than or equal to</option>`+
                 `<option value="lte" ${selected_option("lte",default_comparison)}>Less than or equal to</option>`+
                 `<option value="equals" ${selected_option("equals",default_comparison)}>Equals</option>`+
                 `<option value="ne" ${selected_option("ne",default_comparison)}>Does not Equal</option>`+
            `</select>`+
          `<input type="text" id="criteria-value" name="criteria-value" value="${default_value}"><br>` +
          `<br><input type="checkbox" id="negated" name="negated">` +
          `<label for="negation-maker">Exclusion?</label><br>` +
          `<button type="button" value="Cancel" id="cancel-criteria">Cancel</button>` +
          `<input type="submit" value="${submit_text}" id="add_cri">` +
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



function setupAjaxWithCSRF(){
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });
}

function loadCriteria(){
    //Get Searchable Criteria List
    $.getJSON("/api/criteria/?searchable=true", function(result){
          criteria_list = result.results;

          $( "#criteria-lookup" ).autocomplete({
            source: criteria_list.map(item=>item.name)
    });
    });
}

function handleLookupFormSubmission(){
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
}


function handleEditCriteria(){
        //Editing a Criteria
    $(document).on( "click",".edit-criteria", function(e) {
        e.preventDefault();
        let criteria = $(this).data('criteria');
        $.getJSON(`/api/criteria_response/${criteria}`, function(result){
            $("#selected-criteria-form").empty();

            let criteria_id = result.criteria;
            let criteria_item = criteria_list.find(item=>criteria_id === item.id);
            let form_template = null;

            if (criteria_item.valueType === 'enter_val_comp'){
                form_template = form_comparison(criteria_item,result)
            }

            if (criteria_item.valueType === 'enter_val_fixed'){
                form_template = form_comparison(criteria_item,result)
            }

            if (criteria_item.valueType ==='yes_no'){
                form_template = form_yes_no(criteria_item,result)
            }

            if (criteria_item.valueType === 'pick_one'){
                form_template = form_select(criteria_item,result)
            }

            if (criteria_item.valueType === 'list'){
                form_template = form_select(criteria_item,result)
            }

            $("#selected-criteria-form").append(form_template);

        });
    });
}

function handleAddCriteria(){
       //Submitting a Criteria
    $(document).on( "submit","#add-criteria", function(e) {
        e.preventDefault();
        let trial_id = $( "#criteria-lookup-form" ).data('trial');
        let criteria_id = $(this).data('criteria');

        let serialized_data = $(this).serializeArray();

        let criteria_value = serialized_data.filter(item=>item.name==='criteria-value')

        if (criteria_value.length > 1){
            criteria_value = criteria_value.map(item=>item.value);
            criteria_value = JSON.stringify(criteria_value)
        }else{
            criteria_value = criteria_value[0].value
        }

        let criteria_comparison = 'equals';

        //check for a comparison value
        if (serialized_data.filter(item=>item.name==='comparison').length > 0){
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

}

function handleUpdateCriteria(){
       //Submitting a Criteria
    $(document).on( "submit","#edit-criteria", function(e) {
        e.preventDefault();

        let trial_id = $( "#criteria-lookup-form" ).data('trial');
        let criteria_id = $(this).data('criteria');
        let id = $(this).data('id');

        let serialized_data = $(this).serializeArray();

        let criteria_value = serialized_data.filter(item=>item.name==='criteria-value')

        if (criteria_value.length > 1){
            criteria_value = criteria_value.map(item=>item.value);
            criteria_value = JSON.stringify(criteria_value)
        }else{
            criteria_value = criteria_value[0].value
        }

        let criteria_comparison = 'equals';

        //check for a comparison value
        if (serialized_data.filter(item=>item.name==='comparison').length > 0){
            let comparison = serialized_data.find(item=>item.name==='comparison');
            criteria_comparison = comparison.value;
        }

        let criteria_data = {
            "id": id,
            "value": criteria_value,
            "comparison": criteria_comparison,
            "criteriaType": "inclusion",
            "negated": false,
            "criteria": criteria_id,
            "trial": trial_id
        };

        console.log(criteria_data);

        $.ajax({
            type: "PUT",
            url: `/api/criteria_response/${id}/`,
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

}





function handleDeleteCriteria(){
        $(document).on( "click",".delete-criteria", function(e) {
        e.preventDefault();
        $("#selected-criteria-form").empty();
        let criteria = $(this).data('criteria');
        let row = $(this).parent().parent();
        //Delete

        $.ajax({
            url: `/api/criteria_response/${criteria}`,
            type: 'DELETE',
            success: function(result) {
                //Remove Row
                console.log("success!",result);
                row.remove();
            }
        });
    });
}

function handleCancel() {
    $(document).on( "click","#cancel-criteria", function(e) {
        e.preventDefault();
        $("#selected-criteria-form").empty();
});
}


//Document Ready
$(function(){
    setupAjaxWithCSRF();
    loadCriteria();
    handleLookupFormSubmission();
    handleEditCriteria();
    handleAddCriteria();
    handleUpdateCriteria();
    handleCancel();
    handleDeleteCriteria();
});
