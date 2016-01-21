
var welcomeView;
var profileView;


setBody = function(view){
  document.getElementById("body").innerHTML = view.innerHTML;
};


window.onload = function(){
  welcomeView = document.getElementById("welcomeView");
  profileView = document.getElementById("profileView");

  setBody(welcomeView);
};

login = function(){
  setBody(profileView);
}

logout = function(){
  setBody(welcomeView);
}
