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
    let default_value = '';
    if (defaults){
        default_value = defaults.value;
    }

    return  `<form name="add-criteria" id="add-criteria" data-criteria="${props.id}">` +
      `<select id="criteria-value" class="criteria-option-select" name="criteria-value" style="width: 100%">`+
      `<option value="Yes" ${selected_option("Yes",default_value)}>Yes</option>`+
      `<option value="No" ${selected_option("No",default_value)}>No</option>`+
      `</select>` +
        `</form>`
}

//add conditions to allow for multiple select
function form_select(props,defaults){
    let select_type = '';
    let option_class = '';
    if (props.valueType === 'list') {
        select_type = 'Multiple';
        option_class = 'multi-option'
    }

    let default_value = '';
    if (defaults){
        default_value = defaults.value;
    }

    return `<form name="add-criteria" id="add-criteria" data-criteria="${props.id}">` +
    `<label class="criteria-response" for="criteria" class="mdb-main-label">Select the Values that Apply </label>` +
    `<select ${select_type} class="criteria-option-select" id="criteria-value" name="criteria-value" style="width: 100%">`+
     props.options.map(option=>`<option class="${option_class}" value="${option}" ${selected_option(option,default_value)}>${option}</option>`) +
    `</select>` +
        `</form>`
}


function form_comparison(props,defaults){
    let default_comparison = null;
    let default_value = '';
    if (defaults){
        default_comparison = defaults.comparison;
        default_value = defaults.value;
    }

      return `<form name="add-criteria" id="add-criteria" data-criteria="${props.id}">` +
    `<select class="criteria-option-select" id="comparison" name="comparison" style="width: 100%">`+
                 `<option value="gte" ${selected_option("gte",default_comparison)}>Greater than or equal to</option>`+
                 `<option value="lte" ${selected_option("lte",default_comparison)}>Less than or equal to</option>`+
                 `<option value="equals" ${selected_option("equals",default_comparison)}>Equals</option>`+
                 `<option value="ne" ${selected_option("ne",default_comparison)}>Does not Equal</option>`+
            `</select>`+
          `<input type="text" id="criteria-value" name="criteria-value" value="${default_value}">` +
        `</form>`
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
    $.getJSON("/api/criteria/", function(result){
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
        $("#criteria-modal-body").empty()
        let criteriaCategory = $("#criteria-lookup").val();
        let criteria_item = criteria_list.find(item=>criteriaCategory === item.name);
        $('#criteria-modal-title').text(criteriaCategory);

        let template = null;

        if (criteria_item.valueType === 'enter_val_comp'){
            template = form_comparison(criteria_item)
        }

        if (criteria_item.valueType === 'enter_val_fixed'){
            template = form_comparison(criteria_item)
        }

        if (criteria_item.valueType ==='yes_no'){
            console.log('yes no')
            template = form_yes_no(criteria_item)
        }

        if (criteria_item.valueType === 'pick_one'){
            template = form_select(criteria_item)
        }

        if (criteria_item.valueType === 'list'){
            template = form_select(criteria_item)
        }

        $("#criteria-submit-button").text("Add");
        $("#criteria-submit-button").data('method',"add");
        $("#criteria-modal-body").append(template);
        $('.criteria-option-select').select2({
            dropdownParent: $('#criteria-modal'),
        });
        $('#criteria-modal').modal('show');


        return false;
    });
}


function handleEditCriteria(){
        //Editing a Criteria
    $(document).on( "click","#edit-button-rect", function(e) {
        e.preventDefault();
        $("#criteria-modal-body").empty()
        let criteria = $(this).data('criteria');
        $.getJSON(`/api/criteria_response/${criteria}`, function(result){
            $("#selected-criteria-form").empty();

            let criteria_id = result.criteria;
            let criteria_item = criteria_list.find(item=>criteria_id === item.id);
            let template = null;

            if (criteria_item.valueType === 'enter_val_comp'){
                template = form_comparison(criteria_item,result)
            }

            if (criteria_item.valueType === 'enter_val_fixed'){
                template = form_comparison(criteria_item,result)
            }

            if (criteria_item.valueType ==='yes_no'){
                template = form_yes_no(criteria_item,result)
            }

            if (criteria_item.valueType === 'pick_one'){
                template = form_select(criteria_item,result)
            }

            if (criteria_item.valueType === 'list'){
                template = form_select(criteria_item,result)
            }

            $("#criteria-submit-button").text("Update");
            $("#criteria-submit-button").data('method',"update");
            $("#criteria-submit-button").data('criteria',result.id);
            $("#criteria-modal-body").append(template);
            $('.criteria-option-select').select2({
                dropdownParent: $('#criteria-modal'),
            });
            $('#criteria-modal').modal('show');

        });
    });
}

function handleSubmitCriteria(){
       //Submitting a Criteria
    $(document).on( "click","#criteria-submit-button", function(e) {
        e.preventDefault();
        let trial_id = $( "#criteria-lookup-form" ).data('trial');
        let criteria_id = $("#add-criteria").data('criteria');
        let criteria_type = $( "#criteria-lookup-form" ).data('type');
        let response_id = null;
        let method = "POST";
        let endpoint = "/api/criteria_response/";
        if ($("#criteria-submit-button").data('method') === 'update'){
            response_id = $("#criteria-submit-button").data('criteria');
            method = "PUT";
            endpoint += `${response_id}/`;
        }

        let serialized_data = $("#add-criteria").serializeArray();

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
            "criteriaType": criteria_type,
            "negated": false,
            "criteria": criteria_id,
            "trial": trial_id
        };

        if (response_id){
            criteria_data["id"] = response_id;
        }


        console.log(criteria_data);
        $.ajax({
            type: method,
            url: endpoint,
            data: JSON.stringify(criteria_data),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data){
                location.reload();
                console.log(endpoint);
                console.log(criteria_data);
            },
            failure: function(errMsg) {
                console.error(errMsg);
            }
        });
        return false
    });

}

function handleDeleteCriteria(){
        $(document).on( "click","#delete-button-rect", function(e) {
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


function handleCriteriaHover(){
    $(document).on('mouseenter', '.criteria-item', function () {
        $(this).find("#edit-button").show();
        $(this).find("#delete-button").show();
    }).on('mouseleave', '.criteria-item', function () {
        $(this).find("#delete-button").hide();
        $(this).find("#edit-button").hide();
    });
}


//Document Ready
$(function(){
    setupAjaxWithCSRF();
    loadCriteria();
    handleLookupFormSubmission();
    handleCriteriaHover();
    handleEditCriteria();
    handleSubmitCriteria();
    handleDeleteCriteria();

});
