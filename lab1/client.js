


var welcomeView;
var profileView;
var userToken;
var userEmail;

setBody = function(view){
  document.getElementById("body").innerHTML = view.innerHTML;
};


window.onload = function(){
  welcomeView = document.getElementById("welcomeView");
  profileView = document.getElementById("profileView");

  setBody(welcomeView);
};

// -------- Show user info


userInfo = function (token, view, email) {
  var returnCode = serverstub.getUserDataByEmail(token,email);
  var userData = returnCode.data;

  if (returnCode.success == false) {
    document.getElementById(view+"error-area").innerHTML = returnCode.message;
  }
  else {
    document.getElementById(view+"error-area").innerHTML = null;

    document.getElementById(view+"info-email").innerHTML = userData.email;
    document.getElementById(view+"info-firstname").innerHTML = userData.firstname;
    document.getElementById(view+"info-lastname").innerHTML = userData.familyname;
    document.getElementById(view+"info-gender").innerHTML = userData.gender;
    document.getElementById(view+"info-city").innerHTML = userData.city;
    document.getElementById(view+"info-country").innerHTML = userData.country;
  }
}

wallData = function(token, view, email) {
  var wallArea = document.getElementById(view+"wallArea");
  var returnCode = serverstub.getUserMessagesByEmail(token, email);
  var posts = returnCode.data;

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
  var post = document.getElementById("home-write-post").value;

  console.log(post);

  serverstub.postMessage(userToken,post,null);

  wallData(userToken, "home-", userEmail);
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

    if (returnCode.success == true){
      userEmail = email;
      userToken = returnCode.data;
      setBody(profileView);
      userInfo(userToken, "home-", userEmail);
      wallData(userToken, "home-", userEmail);
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

var otherUserEmail;

browseUsername = function() {
  otherUserEmail = document.getElementById("browse-username-form").value;

  userInfo(userToken, "browse-", otherUserEmail);
  wallData(userToken, "browse-", otherUserEmail);
}

browseWritePost = function() {
  var content = document.getElementById("browse-write-post").value;

  var returnCode = serverstub.postMessage(userToken, content, otherUserEmail);

  if (!returnCode.success) {
    document.getElementById("browse-post-error-area").innerHTML = returnCode.message;
  }
  else {
    document.getElementById("browse-post-error-area").innerHTML = null;
    wallData(userToken,"browse-", otherUserEmail);
  }

}
