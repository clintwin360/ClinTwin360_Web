var qtyTotal = 0;
var priceTotal = 0;

function updateForm() {
    var criteria = document.getElementById("comparison-0").textContent;
    // console.log(criteria);
    var value = document.getElementById("criteria-response-0").value;
    // console.log(value);
    var comparison;

    // For yes/no questions set comparison to "---"
    if (value != ">=" || value != "<="  || value != "=" || value != "≠") {
      comparison = "---";
    } else {
      comparison = document.getElementById("comparison-selected").value;
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

}
