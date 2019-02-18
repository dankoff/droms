$(document).ready(function() {

  var checkedVals = JSON.parse(localStorage.getItem('checkedVals')) || {};
  var $cbs = $("#filter :checkbox");

  $('a').on("click", function(){
    localStorage.removeItem("checkedVals");
  });

  $cbs.on("change", function(){
    $cbs.each(function(){
      checkedVals[this.id] = this.checked;
    });
    localStorage.setItem("checkedVals", JSON.stringify(checkedVals));
    $('#filter').submit();
  });

  $.each(checkedVals, function(id, state) {
    $("#" + id).prop('checked', state);
  });

});
