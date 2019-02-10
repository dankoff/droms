$(document).ready(function() {
  // datepicker ui
  $('#date').datepicker({
    dateFormat: 'yy-mm-dd',
    maxDate: +0,
    changeMonth: true,
    changeYear: true
  }).datepicker('setDate', new Date());

  function loadOrders() {
    var aDate = $('#date').val();
    $.getJSON(ordersURL, {
      selDate: aDate
    }, function(data) {
      $('#tblOrder tbody').empty();
      $.each(data, function(i, o) {
        var $tr = $('<tr>').append(
          $('<td>').append($('<a href="#"></a>').attr('id', 'order' + o.id).text(o.id)),
          $('<td>').text(o.tableNo),
          $('<td>').text(o.created)
        );
        $('#tblOrder tbody').append($tr);
      });
    });
    return false;
  }

  // load orders on datepicker load
  $(window).on('load', loadOrders);

  // change date event
  $('#date').on('change', function() {
    $('#tblItem tbody').empty();
    loadOrders();
  });

  // reload orders every 3 secs
  window.setInterval(loadOrders, 3000);

  // select order event
  $("#tblOrder tbody").on('click', 'a', function() {
    $.getJSON(showOrderURL, {
      orderId: $(this).text()
    }, function(data) {
      $('#tblItem tbody').empty();
      $.each(data, function(i, o) {
        var $tr;
        if (i === 0) {
          $tr = $('<tr>').append(
            $('<td>').text(o.orderId),
            $('<td>').text(o.tableNo),
            $('<td>').text(o.created),
            $('<td>'),
            $('<td>'),
            $('<td>')
          );
          $('#tblItem tbody').append($tr);
        }

        var $diet = $('<td>');
        if (o.diet) {
          $diet.append($('<img width="50" height="35">').attr('src',
                            '../static/images/!.png'.replace('!', o.diet))
                            .attr('alt', o.diet).attr('title', o.diet));
        }
        var $spicy = $('<td>');
        if (o.spicy) {
          $spicy.append($('<img width="50" height="35">').attr('src',
                            '../static/images/!.png'.replace('!', o.spicy))
                            .attr('alt', o.spicy).attr('title', o.spicy));
        }

        $tr = $('<tr>').append(
          $('<td>'),
          $('<td>'),
          $('<td>'),
          $('<td>').append($('<b>').text(o.quantity + ' x ')).append($('<i>').text(o.name)),
          $diet,
          $spicy
        );
        $('#tblItem tbody').append($tr);
      });
    });
    return false;
  });
});
