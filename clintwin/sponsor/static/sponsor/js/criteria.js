var searchableCriteria = [];
var currentPage = 1;

$(function(){
      $.getJSON("/api/criteria/", function(result){
          var pages = Math.ceil(result.count / 10);
          console.log(pages);
          $.each(result.results, function(i, field){
            if (field.searchable){
                searchableCriteria.push(field.name);
            }
        });
        while (currentPage < pages){
            currentPage++;
            $.getJSON("/api/criteria/?page="+currentPage, function(result){
                $.each(result.results, function(i, field){
                    if (field.searchable){
                        searchableCriteria.push(field.name);
                    }
                });
      });
    }
    console.log(searchableCriteria);
    });
    });
