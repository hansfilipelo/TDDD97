
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

  var welcomeView = document.getElementById("welcomeView");

  setBody(welcomeView);
}


// ------------
// sign up

signUp = function(){
  var email = document.getElementById("signup-email").value;
  var firstName = document.getElementById("signup-firstname").value;
  var lastName = document.getElementById("signup-lastname").value;
  var gender = document.getElementById("signup-gender").value;
  var city = document.getElementById("signup-city").value;
  var country = document.getElementById("signup-country").value;

  var password = document.getElementById("signup-password").value;
  var repeatPassword = document.getElementById("signup-repeat-password").value;
  var errorArea = document.getElementById("signUpErrorArea");

  if (password.length < 7) {
    errorArea.innerHTML = "Password need to be at least 7 characters.";
  }
  else if ( password != repeatPassword) {
    errorArea.innerHTML = "Passwords does not match!";
  }
  else{ // Sign up!

    var newUser = {
      "email":email,
      "password":password,
      "firstname":firstName,
      "familyname":lastName,
      "gender":gender,
      "city":city,
      "country":country
    }

    var returnCode = serverstub.signUp(newUser);

    if (returnCode.success == true){
      errorArea.innerHTML = "signUp succeeded."
    }
    else{
      errorArea.innerHTML = returnCode.message;
    }

  }
}
