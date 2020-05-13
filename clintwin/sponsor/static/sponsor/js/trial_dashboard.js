
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





function registerDeleteTrial(){
        $("#delete-trial-link").click(function() {
        let id = $("#selected-trial-header").data('trial');
        Swal.fire({
          title: 'Are you sure?',
          text: "You won't be able to revert this!",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Yes, delete it!',
          preConfirm: (login) => {
            return fetch(`/api/trials/${id}/`,{
                method: 'DELETE',
                credentials: 'same-origin',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
            })
              .then(response => {
                if (!response.ok) {
                  throw new Error(response.statusText)
                }
              })
              .catch(error => {
                Swal.showValidationMessage(
                  `Request failed: ${error}`
                )
              })
          },
          allowOutsideClick: () => !Swal.isLoading()
        }).then((result) => {
          if (result.value) {
                $(`#trial-card-${id}`).remove()
                let key = $(this).val();
                let order = $(".set-order:visible").data("order");
                sortTrials(key,order);
            Swal.fire(
              'Deleted!',
              'Your file has been deleted.',
              'success'
            )
          }
        })
    })
}

function setupTrialFiltering(){
    $("#trial-filter").select2({
        placeholder: "Filter",
        allowClear: true});

    $("#trial-filter").change(function() {
        let status = $(this).val();
        let url = `/api/trials/`;

        switch (status) {
            case 'Virtual':
                let is_virtual = $(this).find(':selected').data('virtual')
                url += `?is_virtual=${is_virtual}`;
                break;
            case 'All':
                break;
            default:
                url += `?status=${status}`;
        }
        console.log(url);
        $.getJSON(url, function(result){
            $("#dashboard-trial-cards").empty();
            $.each(result.results, function(i, field){
                add_trial_card(field);
                });
            update_trial_details(result.results[0])
            get_trial_criteria(result.results[0].id)
        });
    });
}

function setupTrialSorting(){
    $("#trial-sort").select2({
        placeholder: "Sort by",
        allowClear: true,
        data: [{id:"title",text:"Title"},
            {id:"recruitmentStartDate",text:"Recruitment Start Date"},
            {id:"recruitmentEndDate",text:"Recruitment End Date"},
            {id:"enrollmentTarget",text:"Target Enrollment"},
            {id:"current_recruitment",text:"Current Recruitment"}]
});
    $("#trial-sort").change(function() {
        let key = $(this).val();
        let order = $(".set-order:visible").data("order");
        sortTrials(key,order);
    });

    $(".set-order").click(function() {
        console.log($(this));
        $("#order-descending").toggle()
        $("#order-ascending").toggle()
        let key = $("#trial-sort").val();
        let order = $(".set-order:visible").data("order");
        sortTrials(key,order);
    });
}

function sortTrials(key,order){
    let selected_card = $(".selected-card");
    let order_modifier = "";
    if (order === 'descending'){
        order_modifier = "-"
    }
    let url = `/api/trials/?ordering=${order_modifier}${key}`;
    $.getJSON(url, function(result){
        $("#dashboard-trial-cards").empty();
        if (result.results.length > 0){
            $.each(result.results, function(i, field){
            add_trial_card(field);
            });


        if ($(selected_card).length == 1){
            let selected_card_id = $(selected_card).data('trial');
            update_trial_details(result.results.find(x=>x.id === selected_card_id));
            get_trial_criteria(selected_card_id);
            selectCard($(`#trial-card-${selected_card_id}`));
        }else{
            update_trial_details(result.results[0]);
            get_trial_criteria(result.results[0].id);
            selectCard($(`#trial-card-${result.results[0].id}`));
        }

        }else{
            $("#dashboard-trial-cards").html(`<div class="col-4"></div><div class="col-4 align-self-center text-center">No Trials. Click the + button to create a new trial</div>`)
            $("#dashboard-trial-details").html(`<div class="row no-trials"><div class="col-4"></div><div class="col-4 align-self-center text-center">Select a Trial to view details</div></div>`)
        }



    });

}

function restoreText(element){
    let str = element.data("origHTML");
    element.html(str);
}

function highlightText(element, word_starts, length) {
    let item = $(element);
    let str = item.data("origHTML");
    if (!str) {
        str = item.html();
        item.data("origHTML", str);
    }
    //console.log(item.data("origHTML"));
    let highlighted_str = "";
    let previous = 0;
    for (let start of word_starts) {
        highlighted_str += str.substr(previous, start-previous);
        highlighted_str += '<span class="hilite">';
        highlighted_str += str.substr(start,length);
        highlighted_str += '</span>';
        previous = start + length;
    }
        highlighted_str += str.substr(previous);
    //str = str.substr(0, start) +
     //   '<span class="hilite">' +
        //str.substr(start, end - start + 1) +
      //  '</span>' +
       // str.substr(end + 1);
    item.html(highlighted_str);
}

function getAllIndexes(arr, val) {
    let indexes = [], i = -1;
    while ((i = arr.indexOf(val, i+1)) != -1){
        indexes.push(i);
    }
    return indexes;
}


function searchTrials(input) {
    let value = $(input).val();
    let filter = value.toUpperCase();
    let cards = $(".card");
    for (let card of cards) {
        let title = $(card).find(".card-title").text().toUpperCase()
        if (title.includes(filter)){
            $(card).show()
            if (filter !== ""){
                let word_starts = getAllIndexes(title,filter);
                let length = filter.length;
                highlightText($(card).find(".card-title"),word_starts,length);
            }else{
                restoreText($(card).find(".card-title"));
            }

        }else{
            $(card).hide()
            restoreText($(card).find(".card-title"));
        }
    }
}

function isVirtualTag(state){
    console.log(state);
    if (state === true){
        return ''
    }else{
        return 'hidden'
    }
}

function trial_card_template(props){
    return `<div id="trial-card-${props.id}"  class="card" data-trial="${props.id}">`+
      `<div class="card-header bg-transparent">`+
        `<div>`+
          `<div id="id-tag">`+
            `<h7 id="trial-id" class="text-right text-muted mt-auto">${props.custom_id}</h7>`+
          `</div>`+

          `<div id="trial-card-tags">`+
            `<span id="trial-card-virtual-tag" class="badge badge-primary" ${isVirtualTag(props.is_virtual)}>virtual</span>`+
            `<span id="trial-card-status-tag" class="badge badge-secondary">${props.status}</span>`+
          `</div>`+
        `</div>`+
      `</div>`+
      `<div class="card-body">`+
        `<h5 class="card-title">${props.title}</h5>`+
      `</div>`+
      `<div class="card-footer bg-transparent">`+
        `<div class="row">`+
          `<div class="card-text col-sm-4">`+
            `<div id="info" class="row">`+
              `<small id="more-info" class="small text-left text-muted">Location: ${props.location}</small>`+
            `</div>`+
            `<div id="info" class="row">`+
              `<small id="more-info" class="small text-left text-muted">Contact: ${props.sponsor.contactPerson}</small>`+
            `</div>`+
            `<div id="info" class="row">`+
              `<small id="more-info" class="small text-left text-muted">Email: ${props.sponsor.email}</small>`+
            `</div>`+
          `</div>`+
          `<div id="target" class="col-sm-4">`+
            `<span id="target-span">`+
              `<h6 class="text-center text-muted">${props.current_recruitment}/${props.enrollmentTarget}</h6>`+
            `</span>`+
          `</div>`+
          `<div id="date" class="col-sm-4">`+
            `<span id="date-span">`+
              `<h6 class="text-muted">${props.recruitmentStartDate} - ${props.recruitmentEndDate}</h6>`+
            `</span>`+
          `</div>`+
        `</div>`+
      `</div>`+
`</div>`
}


function trialDetailsTemplate(props){
    return          `<div>`+
                    `<div class="d-flex flex-row justify-content-center">`+
                        `<div class="title-left"></div>`+
                        `<h2 id="dashboard-trial-title" class="text-center">${props.title}</h2>`+
                        `<div class="title-right"><sup id="dashboard-virtual-tag" class="bg-primary rounded text-white tag">virtual</sup></div>`+
                    `</div>`+
                    `<h5 class="text-muted text-center"><span id="dashboard-trial-start-date">${props.recruitmentStartDate}</span> - <span id="dashboard-trial-end-date">${props.recruitmentEndDate}</span></h5>`+
                `</div>`+
                `<div>`+
                        `<h6>Objective</h6>`+
                        `<p id="dashboard-objective-text" class="text-muted">${props.objective}</p>`+
                        `<h6>Description</h6>`+
                        `<p id="dashboard-description-text" class="text-muted">${props.description}</p>`+
                        `<h6>URL</h6>`+
                        `<a id="dashboard-url-text" href="${props.url}">${props.url}</a>`+
                    `<br>`+
                    `<br>`+
                `<h6>Criteria</h6>`+
                        `<strong>Inclusion</strong>`+
                        `<ul id="dashboard-inclusion-criteria">`+
                        `</ul>`+
                        `<strong>Exclusion</strong>`+
                        `<ul id="dashboard-exclusion-criteria">`+
                        `</ul>`+
                `</div>`
}

function update_trial_details(props){
    $("#dashboard-trial-details").html(trialDetailsTemplate(props));
    $("#selected-trial-header").data('trial',props.id);
    if(props.is_virtual == true){
        $("#dashboard-virtual-tag").show()
        $("#virtual-question-link").show()
    }else{
        $("#dashboard-virtual-tag").hide()
        $("#virtual-question-link").hide()
    }
    console.log("status",props);
    if (props.status === "Active Recruitment"){
        $("#start-trial-link").hide()
        $("#end-trial-link").show()
        $("#criteria-trial-link").hide()
        $("#update-trial-link").hide()
    } else if (props.status === "Recruitment Ended"){
        $("#start-trial-link").hide()
        $("#end-trial-link").hide()
        $("#criteria-trial-link").hide()
        $("#update-trial-link").hide()
    } else if (props.status === "Draft"){
        $("#start-trial-link").show()
        $("#criteria-trial-link").show()
        $("#update-trial-link").show()
        $("#end-trial-link").hide()
    } else {
        //invalid status
        return
    }
}

function get_trial_criteria(id){
    $.getJSON(`/api/criteria_response/?trial=${id}`, function(result){
      //console.log(result);
      update_trial_criteria(result.results)
    });
}

function get_trial_details(id){
    //console.log("getting details")
    $.getJSON(`/api/trials/${id}/`, function(result){
        //console.log(result);
        update_trial_details(result)
        get_trial_criteria(id)
    });
}


function update_trial_criteria(props){
    let inclusion_criteria = props.filter(x=>x.criteriaType === "inclusion");
    let exclusion_criteria = props.filter(x=>x.criteriaType === "exclusion");
    let inclusion_list_items = inclusion_criteria.map(x=>`<li>${x.criteria.name} ${x.comparison} ${x.value}</li>`).join('');
    let exclusion_list_items = exclusion_criteria.map(x=>`<li>${x.criteria.name} ${x.comparison} ${x.value}</li>`).join('');
    $("#dashboard-inclusion-criteria").html(inclusion_list_items);
    $("#dashboard-exclusion-criteria").html(exclusion_list_items);
}

function add_trial_card(props){
    $("#dashboard-trial-cards").append(trial_card_template(props));
}

function registerStartTrial() {
        $("#start-trial-link").click(function() {
        let id = $("#selected-trial-header").data('trial');
        let data = {"status":"Active Recruitment"};
        Swal.fire({
          title: 'Do you want to start recruitment for this trial?',
          text: "You won't be able to revert this!",
          icon: 'info',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Start Recruiting',
          preConfirm: (login) => {
            return fetch(`/api/trials/${id}/`,{
                method: 'PUT',
                credentials: 'same-origin',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            })
              .then(response => {
                if (!response.ok) {
                  throw new Error(response.statusText)
                }
              })
              .catch(error => {
                Swal.showValidationMessage(
                  `Request failed: ${error}`
                )
              })
          },
          allowOutsideClick: () => !Swal.isLoading()
        }).then((result) => {
          if (result.value) {
              $(`#trial-card-${id}`).find("#trial-card-status-tag").text("Active Recruitment");
              get_trial_details(id);
            Swal.fire(
              'Recruitment Begun!',
              'Your trial is now recruiting',
              'success'
            )
          }
        })
    });
}

function registerEndTrial() {
        $("#end-trial-link").click(function() {
        let id = $("#selected-trial-header").data('trial');
        let data = {"status":"Recruitment Ended"};
        Swal.fire({
          title: 'Do you want to end recruitment for this trial?',
          text: "You won't be able to revert this!",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'End Recruiting',
          preConfirm: (login) => {
            return fetch(`/api/trials/${id}/`,{
                method: 'PUT',
                credentials: 'same-origin',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            })
              .then(response => {
                if (!response.ok) {
                  throw new Error(response.statusText)
                }
              })
              .catch(error => {
                Swal.showValidationMessage(
                  `Request failed: ${error}`
                )
              })
          },
          allowOutsideClick: () => !Swal.isLoading()
        }).then((result) => {
          if (result.value) {
              $(`#trial-card-${id}`).find("#trial-card-status-tag").text("Recruitment Ended");
              get_trial_details(id);
            Swal.fire(
              'Recruitment Ended!',
              'Your trial has ended recruitment',
              'success'
            )
          }
        })
    })
}

function registerQuestionUpload() {
    $("#virtual-question-link").click(function() {
        let id = $("#selected-trial-header").data('trial');
        window.location.href = `/sponsor/trial/${id}/question_upload/`;
    })
}

function registerUpdateTrial() {
    $("#update-trial-link").click(function() {
        let id = $("#selected-trial-header").data('trial');
        window.location.href = `/sponsor/updatetrial/${id}`;
    })
}


function registerEditCriteria() {
    $("#criteria-trial-link").click(function() {
        let id = $("#selected-trial-header").data('trial');
        window.location.href = `/sponsor/trial/${id}/criteria/inclusion/`;
    })
}


function selectCard(card){
    if ($(card).hasClass("selected-card")){
        return;
    }
    $(".selected-card").css('background-color', 'white');
    $(".selected-card").removeClass('selected-card');
    $(card).addClass('selected-card');
    if ($('.selected-card:hover').length > 0){
        $(card).css('background-color', '#62bbff');
    }else{
        $(card).css('background-color', '#98d9ff');
    }
    get_trial_details($(card).data('trial'));
}




$(function(){
    let key = $("#trial-sort").val();
    let order = $(".set-order:visible").data("order");
    sortTrials(key,order);



    $(document).on( "mouseover",".card", function() {
        if ($(this).hasClass("selected-card")){
            $(this).css('background-color', '#62bbff');
        }else{
            $(this).css('background-color', '#aeaeae');
        }

    });
    $(document).on( "mouseleave",".card", function() {
        console.log("MOUSE OOUT")
        if ($(this).hasClass("selected-card")){
            $(this).css('background-color', '#98d9ff');
        }else{
            $(this).css('background-color', 'white');
        }
    });




    $(document).on( "click",".card", function() {
        selectCard($(this));
    });


    registerEditCriteria();
    registerStartTrial();
    registerEndTrial();
    registerUpdateTrial();
    registerQuestionUpload();
    registerDeleteTrial();

    setupTrialSorting()
    setupTrialFiltering();

    $("select").on("select2:clear", function (evt) {
  $(this).on("select2:opening.cancelOpen", function (evt) {
    evt.preventDefault();

    $(this).off("select2:opening.cancelOpen");
  });
});

});
