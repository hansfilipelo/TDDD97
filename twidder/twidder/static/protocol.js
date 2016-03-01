// Constants extracting data for call
_CALL_STRING_ = "callstring"

_USERNAME_ = "email"
_PASSWORD_ = "password"
_FIRST_NAME_ = "firstname"
_FAMILY_NAME_ = "familyname"
_GENDER_ = "gender"
_CITY_ = "city"
_COUNTRY_ = "country"

_TOKEN_ = "token"
_MY_EMAIL_ = "my_email"
_TO_EMAIL_ = "to_email"
_CONTENT_ = "content"

_OLD_PASSWORD_ = "old_password"
_NEW_PASSWORD_ = "new_password"

// -----
// Available paths
_SIGN_IN_PATH_ = "/sign_in"
_SIGN_UP_PATH_ = "/sign_up"
_SIGN_OUT_PATH_ = "/sign_out"
_USERMESSAGES_PATH_ = "/usermessages"
_USERMESSAGES_BY_EMAIL_PATH_ = "/usermessages/"
_USERDATA_PATH_ = "/userdata"
_USERDATA_BY_EMAIL_PATH_ = "/userdata/"
_POST_MESSAGE_PATH_ = "/post_message/"
_CHANGE_PASSWORD_PATH_ = "change_password"

// -------------------------------------

function xhttpReq(callbackFunction, data){
  var xhttp = new XMLHttpRequest()

  // Prepare request
  switch(data._CALL_STRING_) {
    case _SIGN_IN_PATH_:
    xhttp.open("POST", data._CALL_STRING_, true);
    xhttp.setRequestHeader(_USERNAME_, data._USERNAME_);
    xhttp.setRequestHeader(_PASSWORD_, data._PASSWORD_);
    break;

    case _SIGN_UP_PATH_:
    xhttp.open("POST", data._CALL_STRING_, true);
    xhttp.setRequestHeader(_USERNAME_, data._USERNAME_);
    xhttp.setRequestHeader(_PASSWORD_, data._PASSWORD_);
    xhttp.setRequestHeader(_FIRST_NAME_, data._FIRST_NAME_);
    xhttp.setRequestHeader(_FAMILY_NAME_, data._FAMILY_NAME_);
    xhttp.setRequestHeader(_GENDER_, data._GENDER_);
    xhttp.setRequestHeader(_CITY_, data._CITY_);
    xhttp.setRequestHeader(_COUNTRY_, data._COUNTRY_);
    break;

    case _SIGN_OUT_PATH_:
    xhttp.open("POST", data._CALL_STRING_, true);
    xhttp.setRequestHeader(_TOKEN_, data._TOKEN_);
    break;

    case _USERMESSAGES_PATH_:
    xhttp.open("POST", data._CALL_STRING_, true);
    xhttp.setRequestHeader(_TOKEN_, data._TOKEN_);
    break;

    case _USERMESSAGES_BY_EMAIL_PATH_:
    xhttp.open("POST", data._CALL_STRING_+data._TO_EMAIL_, true);
    xhttp.setRequestHeader(_TOKEN_, data._TOKEN_);
    break;

    case _USERDATA_PATH_:
    xhttp.open("POST", data._CALL_STRING_, true);
    xhttp.setRequestHeader(_TOKEN_, data._TOKEN_);
    break;

    case _USERDATA_BY_EMAIL_PATH_:
    xhttp.open("POST", data._CALL_STRING_+data._TO_EMAIL_, true);
    xhttp.setRequestHeader(_TOKEN_, data._TOKEN_);
    break;

    case _POST_MESSAGE_PATH_:
    xhttp.open("POST", data._CALL_STRING_+data._TO_EMAIL_, true);
    xhttp.setRequestHeader(_TOKEN_, data._TOKEN_);
    xhttp.setRequestHeader(_MY_EMAIL_, data._MY_EMAIL_);
    xhttp.setRequestHeader(_CONTENT_, data._CONTENT_);
    break;

    case _CHANGE_PASSWORD_PATH_:
    xhttp.open("POST", data._CALL_STRING_, true);
    xhttp.setRequestHeader(_TOKEN_, data._TOKEN_);
    xhttp.setRequestHeader(_OLD_PASSWORD_, data._OLD_PASSWORD_);
    xhttp.setRequestHeader(_NEW_PASSWORD_, data._NEW_PASSWORD_);
    break;
  }

  // Set callBackFunction
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      callbackFunction(JSON.parse(xhttp.responseText));
    }
  }

  // Send prepared request
  xhttp.send();
}
