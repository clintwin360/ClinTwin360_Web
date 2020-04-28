


function trial_card_template(props){
    console.log(props);
    return `<div class="card mt-2" data-trial="${props.id}">`+
  `<div class="card-body">`+
      `<div class="row">`+
      `<div class="col-9">`+
        `<h5 class="card-title">${props.title}`+
        `<small class="text-muted">4/1/2020 - 4/1/2021</small>`+
        `</h5>`+
      `</div>`+
      `<div class="col-3">`+
        `<h5 class="text-muted text-right">100/500</h5>`+
      `</div>`+
      `</div>`+
    `<p class="card-text"></p>`+
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
      update_trial_details(result.results[1])
      get_trial_criteria(result.results[1].id)
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
    get_trial_details($(this).data('trial'))
});

});



