
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
    console.log(item.data("origHTML"));
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

function searchTrials() {
    let value = $("#trial-search").val();
    let filter = value.toUpperCase();
    console.log("filter",filter);
    let cards = $(".card");
    for (let card of cards) {
        let title = $(card).find(".card-title").text().toUpperCase()
        console.log(title,filter,title.includes(filter));
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


function trial_card_template(props){
    console.log(props);
    return `<div id="trial-card-${props.id}" class="card mt-2" data-trial="${props.id}">`+
  `<div class="card-body">`+
      `<div class="row">`+
      `<div class="col-9">`+
        `<h6 class="card-title">${props.title}`+
        `</h6>`+
        `<small class="text-muted">${props.recruitmentStartDate} - ${props.recruitmentEndDate}</small>`+
      `</div>`+
      `<div class="col-3">`+
        `<sup id="virtual-tag" class="bg-primary rounded text-white tag">virtual</sup>`+
        `<sup id="virtual-tag" class="bg-primary rounded text-white tag">${props.status}</sup>`+
        `</div>`+
        `<h5 class="text-muted text-right mt-auto">${props.current_recruitment}/${props.enrollmentTarget}</h5>`+
  `</div>`+
`</div>`
}


function row_template(props){
    let template = "" +
        "<tr id=\"trial-"+ props.id +"\" class=\"clickable-row\">\<" +
        "td>"+props.title+"</td>" +
        "<td>"+props.sponsor.organization+"</td>" +
        "<td>"+props.enrollmentTarget+"</td>" +
        "</tr>";
    return template;
}

function update_trial_details(props){
    $("#dashboard-trial-title").text(props.title)
    $("#dashboard-objective-text").text(props.objective);
    $("#dashboard-description-text").text(props.description);
    $("#selected-trial-header").data('trial',props.id);
}

function get_trial_criteria(id){
    $.getJSON(`/api/criteria_response/?trial=${id}`, function(result){
      console.log(result);
      update_trial_criteria(result.results)
    });
}

function get_trial_details(id){
    console.log("getting details")
    $.getJSON(`/api/trials/?id=${id}`, function(result){
      console.log(result);
      update_trial_details(result.results[0])
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
    console.log("clicked!!" ,$(this).data('trial'));
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

});



