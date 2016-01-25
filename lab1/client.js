
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

// ------------
// login / logout

login = function(){
  var email = document.getElementById("email").value;
  var password = document.getElementById("password").value;

  var errorArea = document.getElementById("signInErrorArea");

  if (password.length < 7){
    errorArea.innerHTML = "Password need to be at least 7 characters.";
  }
  else{
    setBody(profileView);
  }
}

logout = function(){

}


// ------------
// sign up

signUp = function(){
  var password = document.getElementById("signup-password").value;
  var repeatPassword = document.getElementById("signup-repeat-password").value;
  var errorArea = document.getElementById("signUpErrorArea");

  if (password.length < 7) {
    errorArea.innerHTML = "Password need to be at least 7 characters.";
  }
  else if ( password != repeatPassword) {
    errorArea.innerHTML = "Passwords does not match!";
  }
  else{
    setBody(welcomeView);
  }
}
