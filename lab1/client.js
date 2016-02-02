


var welcomeView;
var profileView;
var userToken;

setBody = function(view){
  document.getElementById("body").innerHTML = view.innerHTML;
};


window.onload = function(){
  welcomeView = document.getElementById("welcomeView");
  profileView = document.getElementById("profileView");

  setBody(welcomeView);
};

// -------- Show user info


userInfo = function () {
  var returnCode = serverstub.getUserDataByToken(userToken);
  var userData = returnCode.data;

  if (returnCode.success == false) {
    document.getElementById("info-area").innerHTML = returnCode.message;
  }
  else {
    document.getElementById("info-email").innerHTML = userData.email;
    document.getElementById("info-firstname").innerHTML = userData.firstname;
    document.getElementById("info-lastname").innerHTML = userData.familyname;
    document.getElementById("info-gender").innerHTML = userData.gender;
    document.getElementById("info-city").innerHTML = userData.city;
    document.getElementById("info-country").innerHTML = userData.country;
  }
}

wallData = function() {
  var returnCode = serverstub.getUserMessagesByToken(userToken);
  var posts = returnCode.data;
  var wallArea = document.getElementById("wallArea");

  if (returnCode.success == false) {
    wallArea.innerHTML = returnCode.message;
  }
  else {
    wallArea.innerHTML = "";

    for (var i = 0; i < posts.length; i++) {
      wallArea.innerHTML += "From: ";
      wallArea.innerHTML += posts[i].writer;
      wallArea.innerHTML += " Message: ";
      wallArea.innerHTML += posts[i].content;
      wallArea.innerHTML += "<br>";
    }
  }

}

writePost = function(){
  var post = document.getElementById("write-post").value;

  console.log(post);

  serverstub.postMessage(userToken,post,null);

  wallData();
}

// ------------
// login / logout

login = function(){
  var email = document.getElementById("email").value;
  var password = document.getElementById("password").value;

  var errorArea = document.getElementById("signInErrorArea");

  if (password.length < 1){
    errorArea.innerHTML = "Password need to be at least 1 character.";
  }
  else{
    var returnCode = serverstub.signIn(email,password);

    if (returnCode.success == true){;
      userToken = returnCode.data;
      setBody(profileView);
      userInfo();
      wallData();
    }
    else{
      errorArea.innerHTML = returnCode.message;
    }
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

  if (password.length < 1) {
    errorArea.innerHTML = "Password need to be at least 1 character.";
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
// -------------
