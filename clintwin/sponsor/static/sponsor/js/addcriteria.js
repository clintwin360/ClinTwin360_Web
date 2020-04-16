// Need to grab th criteria entered and populate the "add criteria detail" page
$(function () {
    // Add Criteria button
    $(".add_btn").modalForm({formURL: "{% url 'add_criteria' %}"});

  });
