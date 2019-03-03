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
      $('#tblOrderComp tbody').empty();
      $('#tblOrderPend tbody').empty();
      $.each(data, function(i, o) {
        var $tr = $('<tr>').append(
          $('<td>').append($('<a href="#"></a>').attr('id', 'order' + o.id).text(o.id)),
          $('<td>').text(o.tableNo),
          $('<td>').text(o.created)
        );
        if (o.completed) {
          $('#tblOrderComp tbody').append($tr);
        } else {
          $tr.append($('<td>').append($('<button type="button">Complete</button>').attr('id', 'btn'+o.id)));
          $('#tblOrderPend tbody').append($tr);
        }
      });
    });
    return false;
  }

  function showOrderDetails() {
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
            $('<td>')
          );
          $('#tblItem tbody').append($tr);
        }

        var $itemDetails = $('<td>').append($('<b>').text(o.name)).append($('<br>')).append($('<p class="desc">').text(o.desc));
        if (o.diet) {
          $itemDetails.append($('<img width="50" height="35">').attr('src',
                            '../static/images/!.png'.replace('!', o.diet))
                            .attr('alt', o.diet).attr('title', o.diet));
        }
        if (o.spicy) {
          $itemDetails.append($('<img width="50" height="35">').attr('src',
                            '../static/images/!.png'.replace('!', o.spicy))
                            .attr('alt', o.spicy).attr('title', o.spicy));
        }

        $tr = $('<tr>').append(
          $('<td>'),
          $('<td>'),
          $('<td>'),
          $itemDetails,
          $('<td>').append(o.quantity)
        );
        $('#tblItem tbody').append($tr);
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
  $("#tblOrderComp tbody").on('click', 'a', showOrderDetails);
  $("#tblOrderPend tbody").on('click', 'a', showOrderDetails);
  $("#tblOrderPend tbody").on('click', 'button', function() {
    $.getJSON(completeOrderURL, {
      orderId: $(this).attr('id').replace('btn', '')
    }).done(function() {
      loadOrders();
    });
    return false;
  });
});
