function updateForm() {
    var criteria = document.getElementById("comparison-0").textContent;
    // console.log(criteria);
    var value = document.getElementById("criteria-response-0").value;
    console.log(value, "value");
    var comparison;

    // Check if first character in value is between 1-10
    if (value.charAt(0) == "1" || value.charAt(0) == "2" || value.charAt(0) == "3" || value.charAt(0) == "4"
      || value.charAt(0) == "5" || value.charAt(0) == "6" || value.charAt(0) == "7" || value.charAt(0) == "8"
      || value.charAt(0) == "9" || value.charAt(0) == "0"){
        comparison = document.getElementById("comparison-selected").value;
      } else { // For yes/no OR multi-select questions set comparison to "---"
        comparison = "=";
      }
    // console.log(comparison);

    var exclusion_var = document.getElementById("negation-maker").checked;
    console.log(exclusion_var);
    var exclusion;
    if (exclusion_var === true){
      exclusion = "Exclusion";
    } else {
      exclusion = "Inclusion";
    }
    console.log(exclusion);


    var table=document.getElementById("criteria-table");
    var row=table.insertRow(-1);
    var criteria_col=row.insertCell(0);
    var value_col=row.insertCell(1);
    var comparison_col=row.insertCell(2);
    var exclusion_col=row.insertCell(3);
    criteria_col.innerHTML=criteria;
    value_col.innerHTML=value;
    comparison_col.innerHTML=comparison;
    exclusion_col.innerHTML=exclusion;

    //Remove the form for the criteria
    $('#criteria_x').remove();

    //Either do a proper POST - send to criteria_response to then call

}
