document.onreadystatechange = function() {
  if (document.readyState === "complete") {
    initApp();
  }
}

function initApp() {
  var btns = document.getElementsByClassName( "add-btn" );
  for(var i = 0; i < btns.length; i++) {
    var btn = btns[i];
    btn.addEventListener('click', addToOrder);
  }

}

function addToOrder(e) {
  var btnEl = e.target;
  var itemEl = btnEl.parentElement.parentElement;
  var item_name = itemEl.children[0].innerHTML.split('-')[0];
  var item_cost = itemEl.children[0].innerHTML.split('-')[1];
  item_cost = parseFloat(cost.replace('£', ''));
  var desc = itemEl.children[1].innerHTML;
  var ul = itemEl.children[2].children[0];
  var item_diet = null;
  var item_spicy = null;
  if (ul.children.length === 1) {
    if (ul.children[0].className === "diet") {
      item_diet = ul.children[0].children[0].getAttribute('alt');
    } else {
      item_spicy = ul.children[0].children[0].getAttribute('alt');
    }
  } else if (ul.children.length === 2) {
    item_diet = ul.getElementsByClassName("diet")[0].children[0].getAttribute('alt');
    item_spicy = ul.getElementsByClassName("spicy")[0].children[0].getAttribute('alt');
  }
  var item_details = {
    name : item_name,
    description : desc,
    cost : item_cost,
    diet : item_diet,
    spicy : item_spicy
  };
}
