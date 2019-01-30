document.onreadystatechange = function() {
  if (document.readyState === "complete") {
    initApp();
  }
}

function initApp() {

   var delete_btns = document.getElementsByClassName( "delete-btn" );
   for (var i = 0; i < delete_btns.length; i++) {
     var delete_btn = delete_btns[i];
     delete_btn.addEventListener('click', removeItem);
   }

}

function removeItem(e) {
  var btnClicked = e.target;
  btnClicked.parentElement.parentElement.remove();
}
