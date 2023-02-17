

const register_url = window.location.origin + "/api/user/register/"

$( "#register_button" ).click(function() {
  var email = $("#email")
  var username = $("#username")
  var password = $("#password")
  var password2 = $("#password2")
  let error_email = $('#error_email')
  let error_empty = $('#error_empty')
  error_empty.css("display", "none")
  let error_username = $('#error_username')
  let error_password = $('#error_password')
  let error_password2 = $('#error_password2')
  if (!email.val() || !username.val() || !password.val() || !password2.val() ) {
    error_empty.text("You should fill in all fields")
    error_empty.css("display", "block")
    return
  }
  $.ajax({
    method: 'post',
    dataType: "json",
    headers: {
      'Content-Type': 'application/json',
    },
    url: register_url,
    data: JSON.stringify({
      "email": email.val(),
      "username": username.val(),
      "password": password.val(),
      "password2": password2.val()
    }),
    success: function(data){   /* функция которая будет выполнена после успешного запроса.  */
	     // alert("SUCCESS. TOKEN IN AUTH"); /* В переменной data содержится ответ от index.php. */
      if (data.access_token) {
        location.reload()
      }
    },
    error: function(data) {
      let detail = data.responseJSON.detail
      error_password2.css('display', "none")
      error_password.css('display', "none")
      error_email.css('display', "none")
      error_username.css('display', "none")
        if (detail) {
          if (detail.email) {
            error_email.text(detail.email)
            error_email.css("display", "block")
          }
          if (detail.username) {
            error_username.text(detail.username)
            error_username.css("display", "block")
          }
          if (detail.password) {
            error_password.text(detail.password)
            error_password.css("display", "block")
            return
          }
          if (detail.mismatch_password) {
            error_password.text(detail.mismatch_password)
            error_password2.text(detail.mismatch_password)
            error_password.css("display", "block")
            error_password2.css("display", "block")
        }
}}})});
