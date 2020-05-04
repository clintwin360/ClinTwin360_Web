
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

function setupTrialFiltering(){
    $("#trial-filter").select2();
    $("#trial-filter").change(function() {
        $("#dashboard-trial-cards").empty()
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
        $.each(result.results, function(i, field){
            update_trial_cards(field);
            });
        update_trial_details(result.results[0])
        get_trial_criteria(result.results[0].id)
        });
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

          `<div id="tag">`+
            `<span id="virtual-tag" class="badge badge-primary" ${isVirtualTag(props.is_virtual)}>virtual</span>`+
            `<span id="virtual-tag" class="badge badge-secondary">${props.status}</span>`+
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
              `<small id="more-info" class="small text-left text-muted">Contact: Eli Lily</small>`+
            `</div>`+
            `<div id="info" class="row">`+
              `<small id="more-info" class="small text-left text-muted">Email: eli@hentech.edu</small>`+
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


function update_trial_details(props){
    $("#dashboard-trial-title").text(props.title)
    $("#dashboard-objective-text").text(props.objective);
    $("#dashboard-description-text").text(props.description);
    $("#dashboard-trial-start-date").text(props.recruitmentStartDate);
    $("#dashboard-trial-end-date").text(props.recruitmentEndDate);
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

function update_trial_cards(props){
    $("#dashboard-trial-cards").append(trial_card_template(props));
}

$(function(){



    $.getJSON("/api/trials/", function(result){
        console.log(result.results);
        $.each(result.results, function(i, field){
            console.log(field);
            update_trial_cards(field);
            });
        update_trial_details(result.results[0])
        get_trial_criteria(result.results[0].id)
    });














      $( ".card" ).hover(
  function() {
    $(this).addClass('mask red').css('cursor', 'pointer');
  }, function() {
    $(this).removeClass('mask red');
  }
);












    $(document).on( "click",".card", function() {
    //console.log("clicked!!" ,$(this).data('trial'));
    get_trial_details($(this).data('trial'));
    get_trial_criteria($(this).data('trial'))
});

    $("#criteria-trial-link").click(function() {
        let id = $("#selected-trial-header").data('trial');
        window.location.href = `/sponsor/trial/${id}/criteria/inclusion/`;
    })

    $("#start-trial-link").click(function() {
        let id = $("#selected-trial-header").data('trial');
        window.location.href = `/sponsor/starttrial/${id}`;
    })

    $("#end-trial-link").click(function() {
        let id = $("#selected-trial-header").data('trial');
        window.location.href = `/sponsor/endtrial/${id}`;
    })

    $("#update-trial-link").click(function() {
        let id = $("#selected-trial-header").data('trial');
        window.location.href = `/sponsor/updatetrial/${id}`;
    })

    $("#virtual-question-link").click(function() {
        let id = $("#selected-trial-header").data('trial');
        window.location.href = `/trial/${id}/question_upload/`;
    })

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
            Swal.fire(
              'Deleted!',
              'Your file has been deleted.',
              'success'
            )
          }
        })
       // window.location.href = `/sponsor/deletetrial/${id}`;
    })


    $("#trial-sort").select2();

    setupTrialFiltering();
});
