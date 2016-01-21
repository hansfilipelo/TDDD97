


setBody = function(view){
  document.getElementById("body").innerHTML = view.innerHTML;
};


window.onload = function(){

  window.alert("Hello TDDD97!");

  var welcomeView = document.getElementById("welcomeView");
  var profileView = document.getElementById("welcomeView");

  setBody(welcomeView);
};
