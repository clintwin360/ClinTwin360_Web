// Function to convert csv to JSON
function csv_to_json(csv){
  var lines=csv.split("\n");
  var result = [];
  var headers=lines[0].split(",");

  for(var i=1;i<lines.length;i++){
    var obj = {};
    var currentline=lines[i].split(",");
    for(var j=0;j<headers.length;j++){
      var curr_line = currentline[j].replace(/""/g, '"');
      var len = curr_line.length;
      obj[headers[j]] = curr_line.replace(/"/, '');
    }
    result.push(obj);
  }

  console.log(result);
  //return result; //JavaScript object
  return JSON.stringify(result); //JSON
}


$(function () {
  $("#upload-file").submit(function(e) {

      console.log("Started ..."); //DEBUG --
      // Prevent default form behaviour
      e.preventDefault();

      var file = document.getElementById("file-uploaded").files[0];

      var reader = new FileReader();
      reader.onload = function (e) {
        var output = document.getElementById("fileOutput");
        var texto = e.target.result;

        //Convert using csv_to_json function
        var json_data = csv_to_json(texto);

        //Post using ajax - commented out
        $.ajax({
            type: "POST",
            url: "/api/virtualtrial_questions/",
            data: json_data,
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
      };

      reader.readAsText(file);

      //Reset Upload Form
      $("#upload-file")[0].reset();

    });
});
