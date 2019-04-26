$(document).ready(function() {
  // datepicker ui
  $('#date').datepicker({
    dateFormat: 'yy-mm-dd',
    maxDate: +0,
    changeMonth: true,
    changeYear: true
  }).datepicker('setDate', new Date());

  function refreshOrders(data) {
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
        if (loggedUser === "Cook") {
          $tr.append($('<td>').append($('<button type="button">Complete</button>').attr('id', 'btn'+o.id)));
        }
        $('#tblOrderPend tbody').append($tr);
      }
    });
  }

  function loadOrders() {
    var aDate = $('#date').val();
    $.getJSON(ordersURL, {
      selDate: aDate
    }, function(data) {
      refreshOrders(data);
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

  function getMessages(msgSource, msgType) {
    $.getJSON(loadMessagesURL, {
      source: msgSource
    }, function(data) {
      var $txt = (msgType === 'out') ? $('#txtOut') : $('#txtInc');
      $txt.val('');
      $.each(data, function(i, o) {
        $txt.val($txt.val() + o.datetime + ': ' + o.msg + '\n\n');
      });
    });
    return false;
  }

  function refreshScreen() {
    loadOrders();
    getMessages(incWorkPlace, 'inc');
    getMessages(msgSrc, 'out');
  }

  // load orders on datepicker load
  $(window).on('load', loadOrders);

  // change date event
  $('#date').on('change', function() {
    $('#tblItem tbody').empty();
    loadOrders();
  });

  function sendMessage(msg, src) {
    $.getJSON(sendMessageURL, {
      message: msg,
      source: src
    }, function(data) {
      var $txtOut = $('#txtOut')
      $txtOut.val('')
      $.each(data, function(i, o) {
        $txtOut.val($txtOut.val() + o.datetime + ': ' + o.msg + '\n\n');
      });
    });
  }

  // call waiter message
  $('#btnCall').on('click', function(){
    sendMessage('Come to the kitchen', 'Kitchen');
    return false;
  });

  // order not ready message
  $('#btnNotRdy').on('click', function() {
    if ($('#tblItem tbody').is(':parent')) {
      $('#actions p').text('');
      var selectedOrderId = $('#tblItem tbody tr:first td:first-child');
      var msg = 'Order ' + selectedOrderId.text() + ' is not ready.'
      sendMessage(msg, 'Kitchen');
    } else {
      $('#actions p').text('Select an order first!');
    }
    return false;
  });

  // order ready message
  $('#btnRdy').on('click', function() {
    if ($('#tblItem tbody').is(':parent')) {
      $('#actions p').text('');
      var selectedOrderId = $('#tblItem tbody tr:first td:first-child');
      var msg = 'Is Order ' + selectedOrderId.text() + ' ready?';
      sendMessage(msg, 'Bar');
    } else {
      $('#actions p').text('Select an order first!');
    }
    return false;
  });

  // reload orders and messages every 3 secs
  window.setInterval(refreshScreen, 3000);

  // select order event
  $("#tblOrderComp tbody").on('click', 'a', showOrderDetails);
  $("#tblOrderPend tbody").on('click', 'a', showOrderDetails);
  $("#tblOrderPend tbody").on('click', 'button', function() {
    var aDate = $('#date').val();
    var ordId = $(this).attr('id').replace('btn', '');
    var msg = "Order " + ordId + " is now ready.";
    $.getJSON(completeOrderURL, {
      orderId: ordId,
      message: msg,
      selDate: aDate,
      source: msgSrc
    }, function(data) {
      refreshOrders(data);
    });
    return false;
  });
});
