


var welcomeView;
var profileView;
var userToken;
var userEmail;
var passWordMinLength = 1;
var view;
var otherUserEmail;

setBody = function(view){
  document.getElementById("body").innerHTML = view.innerHTML;
};


window.onload = function(){
  welcomeView = document.getElementById("welcomeView");
  profileView = document.getElementById("profileView");

  setBody(welcomeView);
};

// -------- Show user info

userInfoCallback = function (returnCode) {
  var userData = returnCode.data;

  if (returnCode.success == false) {
    document.getElementById(view+"error-area").innerHTML = returnCode.message;
  }
  else {
    if (view == "browse-") {
      document.getElementById(view+"error-area").innerHTML = null;
    }
    document.getElementById(view+"info-area").style.display = "block";
    document.getElementById(view+"info-email").innerHTML = userData.email;
    document.getElementById(view+"info-firstname").innerHTML = userData.firstname;
    document.getElementById(view+"info-lastname").innerHTML = userData.familyname;
    document.getElementById(view+"info-gender").innerHTML = userData.gender;
    document.getElementById(view+"info-city").innerHTML = userData.city;
    document.getElementById(view+"info-country").innerHTML = userData.country;
  }
}

function userInfo(token, currentView, email){
  view = currentView;

  xhttpReq(userInfoCallback, {_CALL_STRING_: _USERDATA_BY_EMAIL_PATH_, _TOKEN_: token, _TO_EMAIL_: email});
}

// ----------------------------

wallDataCallback = function(returnCode) {
  var wallArea = document.getElementById(view+"wall-area");
  var posts = returnCode.data;

  if (returnCode.success == false) {
    wallArea.innerHTML = returnCode.message;
  }
  else {
    wallArea.innerHTML = null;
    document.getElementById(view+"entire-wall-area").style.display = "block";

    for (var i = 0; i < posts.content.length; i++) {
      wallArea.innerHTML += "From: ";
      wallArea.innerHTML += posts.writer[i];
      wallArea.innerHTML += " Message: ";
      wallArea.innerHTML += posts.content[i];
      wallArea.innerHTML += "<br>";
    }
  }
}

function wallData(token, currentView, email){
  view = currentView;

  xhttpReq(wallDataCallback, {_CALL_STRING_: _USERMESSAGES_BY_EMAIL_PATH_, _TO_EMAIL_: email, _TOKEN_: token});
}

// ----------------------------

function writePostCallback(returnCode){
  wallData(userToken, "home-", userEmail);
}

writePost = function(){
  var post = document.getElementById("home-write-post").value;

  xhttpReq(writePostCallback, {_CALL_STRING_: POST_MESSAGE_PATH_, _TOKEN_: userToken, _TO_EMAIL_: otherUserEmail, _MY_EMAIL_: userEmail});
}

// ------------signIn(email,password);
// login / logout

loginCallBack = function(returnCode){
  var email = document.getElementById("email").value;
  var errorArea = document.getElementById("signInErrorArea");

  if (returnCode.success == true){
    userEmail = email;
    userToken = returnCode.data;
    setBody(profileView);
    userInfo(userToken, "home-", userEmail);
    userInfo(userToken, "account-", userEmail);
    wallData(userToken, "home-", userEmail);
  }
  else{
    errorArea.innerHTML = returnCode.message;
  }
}

function login(){
  var email = document.getElementById("email").value;
  var password = document.getElementById("password").value;
  var errorArea = document.getElementById("signInErrorArea");

  if (password.length < passWordMinLength){
    errorArea.innerHTML = "Password need to be at least " + passWordMinLength + " characters.";
  }
  else{
    xhttpReq(loginCallBack, {_CALL_STRING_: _SIGN_IN_PATH_, _USERNAME_: email, _PASSWORD_: password});
  }
}

// ------

logoutCallBack = function(returnCode){
  var welcomeView = document.getElementById("welcomeView");
  setBody(welcomeView);
}

function logout(){
  xhttpReq(logoutCallBack, {_CALL_STRING_: _SIGN_OUT_PATH_, _TOKEN_: userToken});
}

// ------------
// sign up

function signUpCallback(returnCode) {
  var errorArea = document.getElementById("signUpErrorArea");

  errorArea.innerHTML = returnCode.message
}

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

  if (password.length < passWordMinLength) {
    errorArea.innerHTML = "Password need to be at least " + passWordMinLength + " characters.";
  }
  else if ( password != repeatPassword) {
    errorArea.innerHTML = "Passwords does not match!";
  }
  else{ // Sign up!

    var newUser = {
      _CALL_STRING_:_SIGN_UP_PATH_,
      _USERNAME_:email,
      _PASSWORD_:password,
      _FIRST_NAME_:firstName,
      _FAMILY_NAME_:lastName,
      _GENDER_:gender,
      _CITY_:city,
      _COUNTRY_:country
    }

    xhttpReq(signUpCallback, newUser);
  }
}
// -------------

browseUsername = function() {
  otherUserEmail = document.getElementById("browse-username-form").value;

  if (otherUserEmail == userEmail) {
    document.getElementById("browse-error-area").innerHTML = "Are you browsing yourself you narcisist you!?";
    return;
  }

  document.getElementById("browse-error-area").innerHTML = null;
  userInfo(userToken, "browse-", otherUserEmail);
  wallData(userToken, "browse-", otherUserEmail);
}

// ------

browseWritePostCallback = function(returnCode) {
  if (!returnCode.success) {
    document.getElementById("browse-post-error-area").innerHTML = returnCode.message;
  }
  else {
    document.getElementById("browse-post-error-area").innerHTML = null;
    wallData(userToken,"browse-", otherUserEmail);
  }
}

function browseWritePost(){
  var content = document.getElementById("browse-write-post").value;

  xhttpReq(browseWritePostCallback, {_CALL_STRING_: _POST_MESSAGE_PATH_, _TO_EMAIL_: otherUserEmail, _MY_EMAIL_: userEmail, _CONTENT_: content, _TOKEN_: userToken})
}

// ----------------------

changePassword = function(){
  var errorArea = document.getElementById("account-error-area");

  var oldPasswordField = document.getElementById("account-old-password");
  var newPasswordField = document.getElementById("account-new-password");
  var repeatPasswordField = document.getElementById("account-repeat-password");

  if (oldPasswordField.value.length < passWordMinLength){
    errorArea.innerHTML = "Password need to be at least " + passWordMinLength + " characters.";
    return;
  }

  if (newPasswordField.value == repeatPasswordField.value) {
    var returnCode = serverstub.changePassword(userToken, oldPasswordField.value, newPasswordField.value);

    if (returnCode.success) {
      newPasswordField.value = null;
      repeatPasswordField.value = null;
      oldPasswordField.value = null;
      errorArea.innerHTML = null;
    }
    else{
      errorArea.innerHTML = returnCode.message;
    }
  }
  else {
    errorArea.innerHTML = "Passwords does not match!"
  }
}
